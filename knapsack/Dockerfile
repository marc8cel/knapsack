FROM python:3.9-slim AS base

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Installer Wine pour exécuter les exécutables Windows sur Linux
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y \
    wine64 wine32

FROM base AS final

WORKDIR /app

COPY --from=base /app /app

COPY . /app

# Vérifier la présence de glpsol.exe et appliquer les permissions
RUN ls -l /app/setup/winglpk-4.65/glpk-4.65/w64/ || echo "glpsol not found!" \
    && if [ -f /app/setup/winglpk-4.65/glpk-4.65/w64/glpsol.exe ]; then chmod +x /app/setup/winglpk-4.65/glpk-4.65/w64/glpsol.exe; else echo "glpsol.exe not found!"; fi

# Utiliser Wine pour exécuter glpsol.exe sur Linux
RUN wine /app/setup/winglpk-4.65/glpk-4.65/w64/glpsol.exe --version || echo "Failed to run glpsol"

CMD ["streamlit", "run", "app.py"]
