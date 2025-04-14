### Alembic

To create a revision:
```commandline
python -m alembic.config revision --autogenerate -m "My message"
```

To upgrade db schema:
```commandline
python -m alembic.config upgrade head
```