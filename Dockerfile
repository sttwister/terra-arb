FROM python:3

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Install pip requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the app
COPY . /app/

EXPOSE 8080

# Run the traaaap
CMD ./main.py
