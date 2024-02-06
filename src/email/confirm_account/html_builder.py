def build_email_confirm_html(url: str):

    html_head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Linguisage Registration</title>
        <style>
            @import url('https://fonts.cdnfonts.com/css/gilroy-bold');

            * {
                padding: 0;
                margin: 0;
                box-sizing: border-box;
                font-family: 'Gilroy', sans-serif;
            }

            .background {
                background: #ffffff;
                color: #5280DB;
                width: 100%;
                flex-direction: column;
                align-items: center;
            }

            header {
                margin: 60px;
                font-size: 50px;
                font-weight: 700;
                color: #5280DB;


            }
            .wrapper {
                margin:  0 auto;
                width: 600px;
            }

            .content {
                font-size: 20px;
                color: #717171;
                font-weight: 450;
            }
        </style>
    </head>
    """
    html_body = f"""
    <body>
    <div class="background">
        <div class="wrapper">
            <header>
                Confirm registration
            </header>

            <div class="content">
                Your email has been provided to register a <a style="text-decoration: none" href="https://www.linguisage.ru"><span style="color:#5280DB; font-weight: 600">Linguisage</span></a>
                account.
                <br>
                <br>
                If it was you, then <a style="text-decoration: none" href="{url}"><span style="color:#5280DB;">click here to confirm</span></a>.
            </div>
            <div class="link"></div>
        </div>
    </div>
    </body>
    </html>
    """

    return html_head + html_body
