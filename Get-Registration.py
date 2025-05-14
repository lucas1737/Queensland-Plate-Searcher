import argparse
import os
import sys
import time
import traceback

def check_registration(plate_number):
    """
    Check vehicle registration details using Selenium with Edge browser
    """
    try:
        # Make sure we have the required packages
        try:
            from selenium import webdriver
            from selenium.webdriver.edge.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
        except ImportError:
            print("Required packages not found. Installing...")
            os.system(f"{sys.executable} -m pip install selenium")
            from selenium import webdriver
            from selenium.webdriver.edge.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
        print(f"Checking registration for plate number: {plate_number}...")
        
        # Setup Edge options
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--window-size=1920,1080")
        
        # Initialize the Edge driver
        driver = webdriver.Edge(options=edge_options)
        
        try:
            # Navigate to the Queensland Transport registration check page
            url = "https://www.service.transport.qld.gov.au/checkrego/application/VehicleSearch.xhtml"
            driver.get(url)
            
            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Save screenshot for debugging
            driver.save_screenshot("initial_page.png")
            print("Initial page screenshot saved as initial_page.png")
            
            # Check if we need to accept Terms of Use
            try:
                # Look for the Terms of Use button using various methods
                terms_button = None
                
                # Try by ID
                try:
                    terms_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "termsForm:acceptButton"))
                    )
                    print("Found Terms of Use button by ID")
                except:
                    # Try by XPath with text
                    try:
                        terms_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
                        print("Found Terms of Use button by text 'Accept'")
                    except:
                        # Try by XPath with class
                        try:
                            terms_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ui-button')]")
                            print(f"Found button with class 'ui-button': {terms_button.text}")
                        except:
                            # Try by any button
                            try:
                                buttons = driver.find_elements(By.TAG_NAME, "button")
                                if buttons:
                                    for button in buttons:
                                        print(f"Found button: {button.text}")
                                        if "accept" in button.text.lower() or "agree" in button.text.lower() or "terms" in button.text.lower():
                                            terms_button = button
                                            print(f"Selected button with text: {button.text}")
                                            break
                            except:
                                print("Could not find any buttons")
                
                # If we found a Terms of Use button, click it
                if terms_button:
                    print("Clicking Terms of Use button...")
                    terms_button.click()
                    
                    # Wait for the page to update after accepting terms
                    time.sleep(2)
                    driver.save_screenshot("after_terms.png")
                    print("Screenshot after accepting terms saved as after_terms.png")
                else:
                    print("No Terms of Use button found. The page might have already loaded or the structure has changed.")
            except Exception as e:
                print(f"Error handling Terms of Use: {e}")
                traceback.print_exc()
            
            # Now try to find the plate number input field
            try:
                plate_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "vehicleSearchForm:plateNumber"))
                )
                print("Found plate number input field by ID")
            except:
                print("Could not find the plate number input field by ID. Trying alternative methods...")
                # Try to find by XPath
                try:
                    plate_input = driver.find_element(By.XPATH, "//input[contains(@id, 'plateNumber')]")
                    print(f"Found plate input field with ID: {plate_input.get_attribute('id')}")
                except:
                    print("Could not find the plate number input field by XPath.")
                    # Try to find by name
                    try:
                        plate_input = driver.find_element(By.NAME, "vehicleSearchForm:plateNumber")
                        print(f"Found plate input field with name: {plate_input.get_attribute('name')}")
                    except:
                        print("Could not find the plate number input field by name.")
                        # Try to find any input field
                        try:
                            inputs = driver.find_elements(By.TAG_NAME, "input")
                            if inputs:
                                print(f"Found {len(inputs)} input fields:")
                                for i, input_field in enumerate(inputs):
                                    input_id = input_field.get_attribute('id')
                                    input_name = input_field.get_attribute('name')
                                    input_type = input_field.get_attribute('type')
                                    print(f"  Input {i+1}: ID={input_id}, Name={input_name}, Type={input_type}")
                                
                                # Try to find an input that looks like it's for a plate number
                                for input_field in inputs:
                                    input_id = input_field.get_attribute('id')
                                    input_name = input_field.get_attribute('name')
                                    if input_id and ('plate' in input_id.lower() or 'rego' in input_id.lower()):
                                        plate_input = input_field
                                        print(f"Selected input field with ID: {input_id}")
                                        break
                                    elif input_name and ('plate' in input_name.lower() or 'rego' in input_name.lower()):
                                        plate_input = input_field
                                        print(f"Selected input field with Name: {input_name}")
                                        break
                            else:
                                print("No input fields found on the page")
                        except:
                            print("Error finding input fields")
                        
                        # If we still can't find it, take a screenshot and raise an exception
                        if 'plate_input' not in locals():
                            driver.save_screenshot("page_structure.png")
                            print("Page structure screenshot saved as page_structure.png")
                            
                            # Dump the page source for debugging
                            with open("page_source.html", "w", encoding="utf-8") as f:
                                f.write(driver.page_source)
                            print("Page source saved as page_source.html")
                            
                            raise Exception("Could not locate the plate number input field")
            
            # Enter the plate number
            plate_input.clear()
            plate_input.send_keys(plate_number)
            
            # Find the search button - using the specific ID you provided
            try:
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "vehicleSearchForm:confirmButton"))
                )
                print("Found search button with ID 'vehicleSearchForm:confirmButton'")
            except:
                print("Could not find the search button with ID 'vehicleSearchForm:confirmButton'. Trying alternative methods...")
                # Try to find by ID with searchButton
                try:
                    search_button = driver.find_element(By.ID, "vehicleSearchForm:searchButton")
                    print(f"Found search button with ID: vehicleSearchForm:searchButton")
                except:
                    print("Could not find the search button by ID 'vehicleSearchForm:searchButton'.")
                    # Try to find by XPath
                    try:
                        search_button = driver.find_element(By.XPATH, "//button[contains(@id, 'confirmButton')]")
                        print(f"Found search button with ID containing 'confirmButton'")
                    except:
                        print("Could not find the search button by XPath with 'confirmButton'.")
                        # Try to find by text
                        try:
                            search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
                            print(f"Found search button with text: Search")
                        except:
                            print("Could not find the search button by text 'Search'.")
                            # Try to find any submit button
                            try:
                                search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                                print(f"Found submit button")
                            except:
                                print("Could not find any submit button.")
                                # Try to find any button
                                try:
                                    buttons = driver.find_elements(By.TAG_NAME, "button")
                                    if buttons:
                                        print(f"Found {len(buttons)} buttons:")
                                        for i, button in enumerate(buttons):
                                            button_id = button.get_attribute('id')
                                            button_text = button.text
                                            print(f"  Button {i+1}: ID={button_id}, Text={button_text}")
                                        
                                        # Try to find a button that looks like a search button
                                        for button in buttons:
                                            button_id = button.get_attribute('id')
                                            button_text = button.text
                                            if button_id and ('search' in button_id.lower() or 'find' in button_id.lower() or 'confirm' in button_id.lower()):
                                                search_button = button
                                                print(f"Selected button with ID: {button_id}")
                                                break
                                            elif button_text and ('search' in button_text.lower() or 'find' in button_text.lower() or 'check' in button_text.lower()):
                                                search_button = button
                                                print(f"Selected button with Text: {button_text}")
                                                break
                                    else:
                                        print("No buttons found on the page")
                                except:
                                    print("Error finding buttons")
                                
                                # If we still can't find it, take a screenshot and raise an exception
                                if 'search_button' not in locals():
                                    driver.save_screenshot("page_structure.png")
                                    print("Page structure screenshot saved as page_structure.png")
                                    raise Exception("Could not locate the search button")
            
            # Click the search button
            print("Clicking search button...")
            search_button.click()
            
            # Wait for results to load
            try:
                # Wait for the results page to load - look for the dl.data elements
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "dl.data"))
                )
                print("Results loaded successfully")
            except:
                print("Timeout waiting for results. Taking screenshot...")
                driver.save_screenshot("timeout.png")
                print("Timeout screenshot saved as timeout.png")
            
            # Take a screenshot of the results page
            driver.save_screenshot("results_page.png")
            print("Results page screenshot saved as results_page.png")
            
            # Check if there's an error message
            error_messages = driver.find_elements(By.CLASS_NAME, "ui-messages-error-detail")
            if error_messages:
                error_text = error_messages[0].text
                print(f"Error: {error_text}")
                with open(f"registration_details_{plate_number}.txt", "w") as f:
                    f.write(f"Error for plate number {plate_number}: {error_text}\n")
                return
            
            # Extract registration details based on the HTML structure you provided
            registration_details = {}
            
            # Get all dl.data elements
            data_lists = driver.find_elements(By.CSS_SELECTOR, "dl.data")
            
            if data_lists:
                print(f"Found {len(data_lists)} data lists")
                
                # Process each data list
                for dl in data_lists:
                    # Get all dt (term) and dd (definition) elements
                    terms = dl.find_elements(By.TAG_NAME, "dt")
                    definitions = dl.find_elements(By.TAG_NAME, "dd")
                    
                    # Pair them up and add to registration_details
                    for i in range(min(len(terms), len(definitions))):
                        term = terms[i].text.strip()
                        definition = definitions[i].text.strip()
                        if term and term not in registration_details:  # Avoid duplicates
                            registration_details[term] = definition
            else:
                print("Could not find any data lists on the page")
                
                # Fallback: try to extract any text content from the page
                try:
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    registration_details["Raw Content"] = body_text
                except:
                    print("Could not extract text from the page")
                    registration_details["Error"] = "Could not extract registration details"
            
            # Print the results
            print(f"\nRegistration details for plate number {plate_number}:")
            print("-" * 50)
            for key, value in registration_details.items():
                print(f"{key}: {value}")
            
            # Save results to a file
            with open(f"registration_details_{plate_number}.txt", "w") as f:
                f.write(f"Registration details for plate number {plate_number}:\n")
                f.write("-" * 50 + "\n")
                for key, value in registration_details.items():
                    f.write(f"{key}: {value}\n")
            
            print(f"\nResults saved to registration_details_{plate_number}.txt")
            
        finally:
            # Close the browser
            driver.quit()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Queensland vehicle registration details")
    parser.add_argument("plate_number", nargs="?", help="The Queensland plate number to check")
    args = parser.parse_args()
    
    # If plate number is provided as command-line argument, use it
    # Otherwise, prompt the user to enter a plate number
    if args.plate_number:
        check_registration(args.plate_number)
    else:
        plate_number = input("Enter the Queensland plate number to check: ")
        check_registration(plate_number)