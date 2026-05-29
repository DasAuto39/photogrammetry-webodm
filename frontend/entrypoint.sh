#!/bin/sh
# Backup the original template if not already done
if [ ! -f /usr/share/nginx/html/index.html.template ]; then
  cp /usr/share/nginx/html/index.html /usr/share/nginx/html/index.html.template
fi

# Restore template
cp /usr/share/nginx/html/index.html.template /usr/share/nginx/html/index.html

# Apply BACKEND_URL variable
if [ -n "$BACKEND_URL" ]; then
  sed -i "s|REPLACE_ME_BACKEND_URL|$BACKEND_URL|g" /usr/share/nginx/html/index.html
else
  sed -i "s|REPLACE_ME_BACKEND_URL|http://localhost:5000|g" /usr/share/nginx/html/index.html
fi

echo "Frontend starting with BACKEND_URL: ${BACKEND_URL:-http://localhost:5000}"
