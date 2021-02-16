
def delete_screenshot_image_on_project_deletion(sender, instance, **kwargs):
    for screenshot in instance.screenshots.all():
        screenshot.delete_actual_image_file()
