from playwright.sync_api import Page

def fill_additional_fields(page: Page):
    """
    Handles filling additional fields in the LinkedIn Easy Apply form.
    """

    print("🔍 Checking for additional fields...")
    
        
    page.pause()
    # Fill text fields
    text_inputs = page.locator("input[type='text']")
    for i in range(text_inputs.count()):
        input_field = text_inputs.nth(i)
        input_name = input_field.get_attribute("Aditya Raj")
        print(f"✏️ Filling text field: {input_name}")
        input_field.fill("My Sample Answer")  # Change this as per field requirement

    # Select dropdowns
    dropdowns = page.locator("select")
    for i in range(dropdowns.count()):
        dropdown = dropdowns.nth(i)
        print("📋 Selecting an option from dropdown")
        dropdown.select_option(value="1")  # Adjust based on field options

    # Check checkboxes
    checkboxes = page.locator("input[type='checkbox']")
    for i in range(checkboxes.count()):
        checkbox = checkboxes.nth(i)
        checkbox.check()
        print("✅ Checkbox checked")

    # Handle file upload (if resume upload is required)
    file_input = page.locator("input[type='file']")
    if file_input.count() > 0:
        print("📁 Uploading resume...")
        file_input.set_input_files("D:/path-to-your-resume.pdf")  # Update path

    print("✅ Additional fields filled successfully!")
