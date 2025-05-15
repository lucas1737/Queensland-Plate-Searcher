import argparse
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

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
                        
                        # If we still can't find it, raise an exception
                        if 'plate_input' not in locals():
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
                                
                                # If we still can't find it, raise an exception
                                if 'search_button' not in locals():
                                    raise Exception("Could not locate the search button")
            
            # Click the search button
            print("Clicking search button...")
            search_button.click()
            
            # Wait for results to load - more flexible approach
            time.sleep(3)  # Give the page time to load
            
            # Check if there's an error message
            error_messages = driver.find_elements(By.CLASS_NAME, "ui-messages-error-detail")
            if error_messages:
                error_text = error_messages[0].text
                print(f"Error: {error_text}")
                return {"Plate Number": plate_number, "Status": "ERROR", "Message": error_text}
            
            # Check for "Registration not found" message
            not_found_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Registration not found')]")
            if not_found_elements:
                print(f"Registration not found for plate number: {plate_number}")
                return {"Plate Number": plate_number, "Status": "NOT FOUND", "Message": "Registration not found"}
            
            # Extract registration details based on the HTML structure
            registration_details = {"Plate Number": plate_number}
            
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
                
                # Make sure we have Status field for the summary
                if "Status" in registration_details:
                    # Status field already exists
                    pass
                else:
                    # Try to determine status from other fields
                    registration_details["Status"] = "REGISTERED" if "Expiry" in registration_details else "UNKNOWN"
            else:
                print("Could not find any data lists on the page")
                
                # Try to extract data from page source directly
                page_source = driver.page_source
                
                # Check if there's any form with registration data
                if "dl class=\"data\"" in page_source:
                    print("Found data lists in page source but couldn't extract with Selenium")
                    
                    # Try a different approach to extract data
                    import re
                    
                    # Extract registration number
                    reg_match = re.search(r'<dt>Registration number\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if reg_match:
                        registration_details["Registration number"] = reg_match.group(1).strip()
                    
                    # Extract VIN
                    vin_match = re.search(r'<dt>Vehicle Identification Number \(VIN\)\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if vin_match:
                        registration_details["Vehicle Identification Number (VIN)"] = vin_match.group(1).strip()
                    
                    # Extract Description
                    desc_match = re.search(r'<dt>Description\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if desc_match:
                        registration_details["Description"] = desc_match.group(1).strip()
                    
                    # Extract Purpose of use
                    purpose_match = re.search(r'<dt>Purpose of use\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if purpose_match:
                        registration_details["Purpose of use"] = purpose_match.group(1).strip()
                    
                    # Extract Status
                    status_match = re.search(r'<dt>Status\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if status_match:
                        registration_details["Status"] = status_match.group(1).strip()
                    
                    # Extract Expiry
                    expiry_match = re.search(r'<dt>Expiry\s*</dt>\s*<dd>([^<]+)</dd>', page_source)
                    if expiry_match:
                        registration_details["Expiry"] = expiry_match.group(1).strip()
                else:
                    # Fallback: try to extract any text content from the page
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    if "Registration not found" in body_text:
                        registration_details["Status"] = "NOT FOUND"
                        registration_details["Message"] = "Registration not found"
                    else:
                        registration_details["Raw Content"] = body_text
                        registration_details["Status"] = "UNKNOWN"
                        registration_details["Message"] = "Could not extract registration details"
            
            # Print the results
            print(f"\nRegistration details for plate number {plate_number}:")
            print("-" * 50)
            for key, value in registration_details.items():
                print(f"{key}: {value}")
            
            return registration_details
            
        finally:
            # Close the browser
            driver.quit()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return {"Plate Number": plate_number, "Status": "ERROR", "Message": str(e)}

def check_multiple_registrations(plate_numbers, max_workers=4):
    """
    Check multiple vehicle registrations concurrently
    
    Args:
        plate_numbers: List of plate numbers to check
        max_workers: Maximum number of concurrent workers (default: 4)
        
    Returns:
        List of registration details dictionaries
    """
    print(f"Checking {len(plate_numbers)} plate numbers with {max_workers} concurrent workers...")
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and collect futures
        futures = {executor.submit(check_registration, plate): plate for plate in plate_numbers}
        
        # Process results as they complete
        for future in futures:
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                plate = futures[future]
                print(f"Error processing plate {plate}: {e}")
                results.append({"Plate Number": plate, "Status": "ERROR", "Message": str(e)})
    
    print(f"Completed checking {len(plate_numbers)} plate numbers")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Queensland vehicle registration details")
    parser.add_argument("plate_number", nargs="*", help="The Queensland plate number(s) to check")
    parser.add_argument("--file", "-f", help="File containing plate numbers (one per line)")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Number of concurrent workers (default: 4)")
    args = parser.parse_args()
    
    plate_numbers = []
    
    # Collect plate numbers from command line arguments
    if args.plate_number:
        plate_numbers.extend(args.plate_number)
    
    # Collect plate numbers from file if specified
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_plates = [line.strip() for line in f if line.strip()]
                plate_numbers.extend(file_plates)
                print(f"Loaded {len(file_plates)} plate numbers from {args.file}")
        except Exception as e:
            print(f"Error reading plate numbers from file: {e}")
    
    # If no plate numbers provided, prompt the user
    if not plate_numbers:
        user_input = input("Enter Queensland plate number(s) separated by commas: ")
        plate_numbers = [p.strip() for p in user_input.split(',') if p.strip()]
    
    # Check if we have any plate numbers to process
    if plate_numbers:
        if len(plate_numbers) == 1:
            # If only one plate number, use the original function
            check_registration(plate_numbers[0])
        else:
            # If multiple plate numbers, use the concurrent function
            results = check_multiple_registrations(plate_numbers, max_workers=args.workers)
            
            # Display a summary of results
            print("\nSummary of Registration Checks:")
            print("-" * 50)
            for result in results:
                plate = result.get("Plate Number", "Unknown")
                if "Error" in result:
                    print(f"{plate}: Error - {result['Error']}")
                elif result.get("Status") == "NOT FOUND":
                    print(f"{plate}: {result['Status']} - {result.get('Message', '')}")
                elif result.get("Status") == "REGISTERED":
                    expiry = result.get("Expiry", "Unknown")
                    description = result.get("Description", "")
                    print(f"{plate}: {result['Status']}, Expiry: {expiry}, Vehicle: {description}")
                else:
                    status = result.get("Status", "Unknown")
                    print(f"{plate}: {status}")
    else:
        print("No plate numbers provided. Exiting.")

