import os
from urllib.parse import urlparse


def hosting_url(request):
    """
    Expose the deployment's public URL to templates as `hosting_url`.
    Priority:
    1) RENDER_EXTERNAL_URL (Render automatically sets this)
    2) HOSTING_URL (manual override)
    3) Build from current request host
    """
    external = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("HOSTING_URL") or ""

    # Render may supply a full URL with path; normalize to scheme://host
    if external:
        try:
            p = urlparse(external)
            if p.scheme and p.netloc:
                external = f"{p.scheme}://{p.netloc}"
        except Exception:
            pass

    if not external and request is not None:
        scheme = "https" if request.is_secure() else "http"
        try:
            host = request.get_host()
        except Exception:
            host = "localhost"
        external = f"{scheme}://{host}"

    return {"hosting_url": external}
