from nicegui import app, ui

from nicegui import ui


@ui.page("/")
def page_index():
    async def show_location():
        response = await ui.run_javascript('''
            return await new Promise((resolve, reject) => {
                if (!navigator.geolocation) {
                    reject(new Error('Geolocation is not supported by your browser'));
                } else {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            resolve({
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                            });
                        },
                        () => {
                            reject(new Error('Unable to retrieve your location'));
                        }
                    );
                }
            });
        ''', timeout=5.0)
        ui.notify(f'Your location is {response["latitude"]}, {response["longitude"]}')

    ui.button('Show location', on_click=show_location)

# ui.run()


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
