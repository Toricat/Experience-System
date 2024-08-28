template_path="c:/Users/hamin/Documents/GitHub/Personal/1_Authentication/server/app/email-templates/build/register_code.html"
with open(template_path, "r", encoding="utf-8") as file:
    template_content = file.read()
    print(template_content)
