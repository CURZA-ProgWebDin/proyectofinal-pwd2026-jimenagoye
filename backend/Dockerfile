FROM python:3.14
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -m -u 1000 appuser
USER appuser  # corre la app como un usuario sin privilegios (mínimo privilegio, más seguro)
EXPOSE 5000
CMD ["flask", "--app", "run.py", "run", "--debug", "--host=0.0.0.0"]  # escucha en todas las interfaces del contenedor