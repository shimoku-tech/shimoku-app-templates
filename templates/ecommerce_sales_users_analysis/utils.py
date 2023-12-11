def super_admin_title(title: str):
    css = """
        .title-section {
            --border-radius: 10px;
            display: flex;
            background: linear-gradient(90deg,  #345DA7 0%, #2e2d88 100%);
            border-radius: var(--border-radius);
            height: 46px;
        }

        .title-section-text {
            color: white;
            display: flex;
            align-items: center;
        }

        .title-section-icon {
            --secondary-accent-500-GW: #FB8500;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg,#FB8500 70px,#0000 0);
            padding: 10px;
            border-top-left-radius: var(--border-radius);
            border-bottom-left-radius: var(--border-radius);
            width: 100px;
        }

        .title-section-icon svg {
            margin-left: 10px;
        }
    """

    html = f"""
        <section class="title-section">
            <div class="title-section-icon">
                <svg width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18 7V18C18 19.1046 17.1046 20 16 20H6C4.89543 20 4 19.1046 4 18V7" stroke="white" stroke-width="2" stroke-linejoin="round"/>
                  <path d="M1 10L9.66207 2.20414C10.4227 1.51959 11.5773 1.51959 12.3379 2.20414L21 10" stroke="white" stroke-width="2" stroke-linecap="round"/>
                  <path d="M8 15C8 13.8954 8.89543 13 10 13H12C13.1046 13 14 13.8954 14 15V20H8V15Z" stroke="white" stroke-width="2"/>
                </svg>
            </div>
            <p class="title-section-text">
                {title}
            </p>

        </section>
    """

    return craft_html(css, html)

def craft_html(css: str, html: str):
    html = f"""
        <head>
            <style>
                {css}
            </style>
        </head>
        {html}
    """

    return html