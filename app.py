from app import create_app

# Instanciate and initialize the app creation
app = create_app()

# Start the app
if __name__ == "__main__":
  app.run()