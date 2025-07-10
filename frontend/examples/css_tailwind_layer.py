from nicegui import ui

ui.add_head_html('''
    <style type="text/tailwindcss">
        @layer components {
            .blue-box {
                @apply bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white;
            }
        }
    </style>
''')

with ui.row():
    ui.label('Hello').classes('blue-box')
    ui.label('world').classes('blue-box')

# ui.run()


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
