from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_twitch_markers():
    # Set up Chrome options to use existing profile
    vod_id = input('Enter the vod id: ')
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:/Users/MSI/AppData/Local/Google/Chrome/User Data")  # Windows path
    chrome_options.add_argument("--headless=new")  # Use headless mode

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Get vod ID from user
        url = f'https://dashboard.twitch.tv/u/georgi_my/content/video-producer/highlighter/{vod_id}'
        
        # Navigate to the page
        driver.get(url)
        
        # Wait for page to load and elements to be present
        wait = WebDriverWait(driver, 10)
        cluster_icons = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "dynamic-pins__cluster-icon")
        ))
        
        # Create ActionChains object for hover actions
        actions = ActionChains(driver)
        
        markers = []
        
        # Hover over each cluster icon and get the marker text
        for icon in cluster_icons:
            try:
                # Scroll element into view
                driver.execute_script("arguments[0].scrollIntoView(true);", icon)
                time.sleep(0.1)  # Brief pause for scroll to complete
                
                # Hover over the element
                actions.move_to_element(icon).perform()
                time.sleep(0.2)  # Wait for tooltip to appear
                
                # Find all VzRGo elements that appear
                marker_elements = driver.find_elements(By.CLASS_NAME, "VzRGo")
                
                # Get text from each VzRGo element
                for element in marker_elements:
                    try:
                        marker_text = element.text
                        if marker_text:  # Only add non-empty markers
                            markers.append(marker_text)
                    except:
                        continue
                
                # Brief pause before moving to next cluster
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing marker: {str(e)}")
        
        return markers
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
        
    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    # Run the script
    markers = get_twitch_markers()
    
    # Print results
    print("\nFound Markers:")
    for i, marker in enumerate(markers, 1):
        print(f"{i}. {marker}")