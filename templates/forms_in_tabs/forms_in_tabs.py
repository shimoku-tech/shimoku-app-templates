import random

import shimoku_api_python as shimoku

from os import getenv


#--------------------AUXILIARY FUNCTIONS--------------------#
def title_for_tab(title: str, image: str):
    images_map = dict(
        up_arrow='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63b70d3e066b7de92c87e0d6_objetivo.svg',
        person='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63b70d3ed31dd23d7f03c557_confirm.svg',
        question_mark='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63b70d3efa39b1480451e0a7_questions.svg',
        calendar='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63b70d3efa39b15f2451e0a6_when.svg',
        clipboard='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63d38d2975ec8b6beff4b627_descarte.svg',
        contact='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63d38d299332c063e44ab858_diagnos.svg',
        line='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63d38d29d6508b3eccc21382_historia.svg',
    )
    return (
        "<head>"
        "<style>.subtitle-block {display: flex; align-items: center;}</style>"
        "<style>.little-subtitle-block {height:48px; width:48px; padding-up: 24px; color:var(--color-white);}</style>"
        "<style>.subtitle {var(--color-black); padding-left: 24px; padding-up: 24px;}</style>"
        "</head>"
        "<div class='subtitle-block'>"
        "<div class='little-subtitle-block'>"
        f"<img src={images_map[image]}>"  # Change url
        "</div>"
        f"<h4 class='subtitle'>{title}</h6>"  # Change subtitle
        "</div>"
    )


#--------------------DASHBOARD FUNCTIONS--------------------#
def create_header(shimoku_client: shimoku.Client):
    header = (
        "<head>"
        "<style>.hero-block"
        "{display: flex; align-items: center; padding: 24px; background-color:transparent;}"
        "</style>"
        # Start styles icon bg
        "<style>.little-head-block"
        "{height:80px; width:80px; border-radius:var(--border-radius-m);"
        "padding:16px; background:var(--color-secondary);"
        "color:var(--color-white);}"
        "</style>"
        # End styles icon bg
        "<style>.title{var(--color-black); padding-left: 24px;}</style>"
        "<style>.button-block{position: absolute; right: 0;}</style>"
        # Start styles button
        "<style>.button"
        "{display: flex; background-color: var(--color-black);"  # Change bg color
        "padding: 16px; border-radius: var(--border-radius-m);"  # Change padding to increase width and height
        "font-size: 14px; color: var(--color-white); box-shadow: var(--box-shadow-m); transition-duration: 0.2s;}"
        ".button:hover{background-color: var(--color-secondary); color: var(--color-white);}"  # Change bg and text hover colors
        "</style>"
        # End styles button
        "</head>"
        "<div class='hero-block'>"
        "<div class='little-head-block'>"
        "<img src='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63d266030485cb25312127b2_usersearch.svg'>"
        "</div>"
        "<h1 class='title'>Forms In Tabs</h1>"
        "</div>"
        "</div>"
    )

    shimoku_client.plt.html(
        html=header, order=0, cols_size=12,
    )


def first_step_tab(shimoku_client: shimoku.Client):
    shimoku_client.plt.set_tabs_index(tabs_index=('Steps', 'First Step'), order=2)

    def first_bentobox():
        shimoku_client.plt.set_bentobox(cols_size=8, rows_size=2)

        shimoku_client.plt.html(
            html=title_for_tab('General Questions', 'question_mark'),
            order=0, rows_size=3, cols_size=22,
            padding='2, 0, 0, 1',
        )

        general_questions_forms_data = {
            'Which problem?': [{
                'mapping': 'whichProblem',
                'fieldName': 'Select a problem',
                'inputType': 'select',
                'options': ['Problem 1', 'Problem 2', 'Problem 3'],
            },
                {
                    'mapping': 'whichProblemIntensity',
                    'fieldName': 'Specify the intensity',
                    'inputType': 'range',
                }],
            'When did it happen?': [{
                'mapping': 'whenDidItHappen',
                'fieldName': 'Select an approximate date range',
                'inputType': 'dateRange',
            }],
            'How did it happen?': [{
                'mapping': 'howDidItHappen',
                'fieldName': 'Describe the problem',
                'inputType': 'text',
            }],
            'Estimated cost?': [{
                'mapping': 'estimatedCost',
                'fieldName': 'Specify the estimated cost',
                'inputType': 'number',
            }],
            'Estimated time to fix?': [{
                'mapping': 'estimatedTimeToFix',
                'fieldName': 'Specify the estimated time to fix in days',
                'inputType': 'number',
            }],
            'How can we contact you?': [{
                'mapping': 'howCanWeContactYouMail',
                'fieldName': 'Specify your email',
                'inputType': 'email',
                'sizeColumns': 11,
            },
                {
                    'mapping': 'howCanWeContactYouTlf',
                    'fieldName': 'Specify your phone number',
                    'inputType': 'tel',
                    'sizeColumns': 11,
                }],
        }

        shimoku_client.plt.set_tabs_index(
            tabs_index=('Questions', list(general_questions_forms_data.keys())[0]), cols_size=22, rows_size=17,
            padding='1,0,0,1', just_labels=True, sticky=False, order=1, parent_tabs_index=('Steps', 'First Step'),
        )

        for question, form_data in general_questions_forms_data.items():
            shimoku_client.plt.change_current_tab(question)
            form_options = {
                'variant': 'autoSend',
                'fields': [
                    {
                        'title': '',
                        'fields': form_data
                    }
                ]
            }
            shimoku_client.plt.input_form(
                options=form_options, order=0, cols_size=22,
                padding=f'{0 if question == "Which problem?" else 1}, 0, 0, 0',
            )

        shimoku_client.plt.pop_out_of_bentobox()
        shimoku_client.plt.set_tabs_index(tabs_index=('Steps', 'First Step'))

    def second_bentobox():
        shimoku_client.plt.set_bentobox(cols_size=4, rows_size=2)
        shimoku_client.plt.html(
            html=title_for_tab('Plan', 'up_arrow'),
            order=4, rows_size=3, cols_size=22,
            padding='2, 0, 0, 1',
        )

        input_forms = {'': [{
            'mapping': 'planSelection',
            'fieldName': 'Select one of the available plans',
            'inputType': 'radio',
            'options': ['Plan A', 'Plan B', 'Plan C', 'Plan D', 'Plan E', 'Plan F', 'Plan G', 'Plan H'],
        }]}

        shimoku_client.plt.generate_input_form_groups(
            order=5, form_groups=input_forms, cols_size=22, rows_size=8,
            padding='1,0,0,1', auto_send=True,
        )
        shimoku_client.plt.pop_out_of_bentobox()

    def third_bentobox():
        shimoku_client.plt.set_bentobox(cols_size=12, rows_size=2)
        shimoku_client.plt.html(
            html=title_for_tab('Previous Experiences', 'clipboard'),
            order=7, rows_size=3, cols_size=22, padding='2, 0, 1, 1',
        )
        input_forms = {'': [
            {
                'mapping': 'previousExperiences',
                'fieldName': 'Have you had previous experiences with this problem?',
                'inputType': 'radio',
                'options': ['Yes', 'No'],
                'sizeColumns': 3,
            },
            {
                'mapping': 'previousExperiencesWhen',
                'fieldName': 'When?',
                'inputType': 'date',
                'sizeColumns': 19,
            },
            {
                'mapping': 'previousExperiencesSolution',
                'fieldName': 'How was it solved?',
                'inputType': 'text'
            }
        ]}

        shimoku_client.plt.generate_input_form_groups(
            order=8, form_groups=input_forms, cols_size=22, rows_size=20,
            padding='0,0,0,1', auto_send=True,
        )
        shimoku_client.plt.pop_out_of_bentobox()

    first_bentobox()
    second_bentobox()
    third_bentobox()


def second_step_tab(shimoku_client: shimoku.Client):
    shimoku_client.plt.set_tabs_index(tabs_index=('Steps', 'Second Step'))

    shimoku_client.plt.html(
        html=title_for_tab("Problem Characteristics", 'question_mark'),
        order=0, rows_size=2, cols_size=12,
    )

    def input_binary_and_select(text, order, options, options_name='Specify'):
        shimoku_client.plt.set_bentobox(cols_size=6, rows_size=2)
        shimoku_client.plt.html(
            html=f"<h6>    </h6> <br> <br>",
            order=order, rows_size=1, cols_size=12,
        )

        text_mapping = text.split(' ')[0]
        input_forms = {'': [{
                'mapping': 'Second Step ' + text_mapping,
                'fieldName': text,
                'inputType': 'radio',
                'options': ['Yes', 'No'],
            },
            {
                'mapping': 'Second Step ' + text_mapping + ' ' + options_name,
                'fieldName': options_name,
                'inputType': 'select',
                'options': options,
                'showSearch': True,
            }
        ]}

        shimoku_client.plt.generate_input_form_groups(
            order=order + 1, form_groups=input_forms, cols_size=22,
            rows_size=14, padding=f'3,0,0,1', auto_send=True,
        )
        shimoku_client.plt.pop_out_of_bentobox()

    input_binary_and_select('Characteristic 1', 2 , ['Option 1', 'Option 2'])
    input_binary_and_select('Characteristic 2', 4 , ['Option 1', 'Option 2'])
    input_binary_and_select('Characteristic 3', 6 , ['Option 1', 'Option 2'])
    input_binary_and_select('Characteristic 4', 8 , ['Option 1', 'Option 2'])
    input_binary_and_select('Characteristic 5', 10, ['Option 1', 'Option 2'])
    input_binary_and_select('Characteristic 6', 12, ['Option 1', 'Option 2'])


# This tab would be shown by default
def results_tab(shimoku_client: shimoku.Client):
    shimoku_client.plt.set_tabs_index(tabs_index=('Steps', 'Results'))

    if not shimoku_client.activities.get_activity(name='Mock Activity'):
        shimoku_client.activities.create_activity(name='Mock Activity')

    shimoku_client.plt.activity_button(
        order=0, activity_name='Mock Activity',
        label='Calculate Results',
        cols_size=2,
        padding='1, 5, 0, 5',
    )

    html = (
        "<head>"
        # Start styles BG
        "<style>.bg-work-v2"
        "{height: 40vh; width: 100%; border-radius: var(--border-radius-m);"
        "margin-top: 16px;"
        "margin-bottom: 32px;"
        "display: flex;"
        "justify-content: center;"
        "align-items: center;"
        "background-size: auto;"
        "background-position: center;"
        "background-repeat: no-repeat;"
        "background-color: var(--color-grey-100);"
        "background-image: url('https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62c814c2b026f0861723e339_illus-work-in-line.svg');"
        "color: var(--color-white);}"
        "</style>"
        # End styles BG
        "<link rel='stylesheet'"
        "href='https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0'/>"
        # Star hint
        "<style>.hint"
        "{display: flex; position: relative; text-align: center;"
        "height: 100%; width:100%; border-radius: var(--border-radius-m); padding:16px;"
        "grid-auto-flow: column; align-items: center;"
        "background-color: var(--color-grey-100);"  # Change BG color
        "color: var(--color-black);}"  # Change Text color
        "</style>"
        # Start icons style
        "<style>.material-symbols-rounded"
        "{display: flex; position: relative;"
        "opacity: 1;"
        "color: var(--color-white);}"
        "</style>"
        # End icons style
        # Start styles text
        "<style>.title-hint"
        "{display: flex; position: relative; width:100%;"
        "padding-left: 16px;"
        "opacity: 1;"
        "color:var(--color-black);}"
        "</style>"
        "<style>.text-hint"
        "{display: flex; position: relative; width:100%;"
        "font-size: 14px;"
        "padding-left: 16px;"
        "opacity: 1;"
        "color:var(--color-black);}"
        "</style>"
        # End hint
        "</head>"

        "<div class='hint'>"
        "<span class='material-symbols-rounded'></span>"
        "<div>"
        "<h3 class='title-hint'> Everything ready?</h3>"
        "<p class='text-hint'>Click the button to get the analysis results</p>"  # Text hint
        "</div>"
        "</div>"
        "<div class='bg-work-v2'>"
        "</div>"
    )

    shimoku_client.plt.html(
        html=html, order=1, rows_size=4, cols_size=8, padding='0,2,0,2',
    )


# This tab would be shown after the activity execution, it would overwrite the previous tab, not it will use mock data
def results_aae_tab(shimoku_client: shimoku.Client):
    shimoku_client.plt.set_tabs_index(tabs_index=('Steps', 'Results (After Activity Execution)'))

    shimoku_client.plt.html(
        html=title_for_tab('Analysis Results', 'person'),
        order=0, rows_size=2, cols_size=12,
    )

    factor_values = [80, 60, 10, 4]

    for i, factor_value in enumerate(factor_values):
        shimoku_client.plt.gauge_indicator(
            order=i*2+1,
            title=f'Factor {i+1}',
            description=f'Description of Factor {i+1}',
            value=factor_value,
            color=i+1,
        )

    factors_through_time = [
        {'date': '2021-01-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-02-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-03-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-04-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-05-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-06-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-07-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-08-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-09-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
        {'date': '2021-10-01', 'factor 1': 80+random.randint(-10, 10), 'factor 2': 60+random.randint(-5, 5), 'factor 3': 10+random.randint(-10, 10), 'factor 4': 4+random.randint(-2, 2)},
    ]

    shimoku_client.plt.html(
        html=title_for_tab('Factors Through Time', 'line'), order=10
    )

    shimoku_client.plt.stacked_area(
        order=11, data=factors_through_time,
        x='date', show_values=['factor 1'],
    )

    shimoku_client.plt.activity_button(
        order=12, activity_name='Mock Activity',
        label='Calculate Results',
        cols_size=2, padding='0, 5, 0, 5',
    )

    shimoku_client.plt.pop_out_of_tabs_group()


def main():
    #---------------- CLIENT INITIALIZATION ----------------#
    api_key: str = getenv('API_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')
    workspace_id: str = getenv('WORKSPACE_ID')
    environment: str = getenv('ENVIRONMENT')

    s = shimoku.Client(
        access_token=api_key,
        universe_id=universe_id,
        environment=environment,
        async_execution=True,
        verbosity='INFO',
    )
    s.set_workspace(workspace_id)
    s.reuse_data_sets()
    s.set_menu_path('Forms In Tabs')
    # s.plt.clear_menu_path()

    #----------------- CREATE DASHBOARD TASKS -----------------#
    create_header(  s)
    first_step_tab( s)
    second_step_tab(s)
    results_tab(    s)
    results_aae_tab(s)

    #----------------- EXECUTE DASHBOARD TASKS -----------------#
    s.run()


if __name__ == '__main__':
    main()
