def show_command(include_args):
    return(f"show ap debug driver-config | inc {include_args}")


print(show_command("EIRP"))