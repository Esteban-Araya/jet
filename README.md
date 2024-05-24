
# BACKEND JET

JET's Backend 

## Deployment
if you want to use this project in local, you will need change in jet/wsgi.py
this line
```bash
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.settings.production")
```
for this
```bash
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.settings.development")
```

To deploy this project run

```bash
  docker-compose up
```

