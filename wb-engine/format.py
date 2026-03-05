import datetime

class Formatter:
    @staticmethod
    def token_registration_style(p_name, p_token, p_type):
        return (
            f"NEW_TOKEN_MADE 🎫\n"
            f"project: {p_name}\n"
            f"token: {p_token}\n"
            f"type: {p_type}\n"
            f"status: active ✅"
        )

    @staticmethod
    def global_var_style(p_name, p_token, var_name, value):
        return (
            f"project: {p_name}\n"
            f"token: {p_token}\n"
            f"---\n"
            f"{var_name}: {value}"
        )

    @staticmethod
    def file_style(p_name, p_token, file_name):
        name_only = file_name.rsplit('.', 1)[0]
        return (
            f"project: {p_name}\n"
            f"token: {p_token}\n"
            f"---\n"
            f"file: {name_only}\n"
            f"###"
        )
