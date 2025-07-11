# bill

## Environment Setup

This project requires environment variables for API tokens and secrets. To set up your environment:

1. Create a `.env` file in the project root with the following variables:
   ```
   INFERENCE_API_TOKEN=your_actual_inference_api_token
   FLASK_SECRET_KEY=your_actual_flask_secret_key
   ```

2. The `.env` file is already in `.gitignore` to prevent secrets from being committed to version control.

3. Run the application using `bin/run.sh` which will automatically source the `.env` file.

## Security Notes

- Never commit the `.env` file to version control
- Keep your API tokens secure and rotate them regularly
- The `bin/run.sh` script will warn you if the `.env` file is missing
