# **AI Mobile Testing Agent**  

The **AI Mobile Testing Agent** automates mobile app testing using **AI-driven step predictions**. It analyzes the screen, suggests actions (click, scroll, type, system), executes them, and adjusts based on user feedback.  

## **How It Works**
1. **User sets a test goal** (e.g., "Test login with invalid credentials").  
2. **AI extracts UI elements** from the current screen.  
3. **AI suggests the next action**, considering past steps and user feedback.  
4. **User approves or rejects the step** before execution.  
5. **Agent executes the action and verifies it using the next screen**.  
6. **Repeats until the test is complete** (or terminated).  

Each test session generates a log file containing **all steps and actions taken**.

---

## **Quickstart**
### **1️⃣ Setup**
Ensure you have the required dependencies installed:  
```bash
pip install -r requirements.txt
```
Make sure you have:
- **Appium Server** running (`http://127.0.0.1:4723` by default).  
- **ADB-enabled device or emulator** connected.  
- **OpenAI API key** set in environment variables (`OPENAI_API_KEY`).  

---

### **2️⃣ Run a New Test**
To start a new test, run:
```bash
python main.py
```
You'll be prompted to **enter a test goal**, e.g.,  
```plaintext
Enter your test goal: Test the search bar functionality
```
The AI will then **analyze the UI, suggest steps, and ask for your approval**.

---

### **3️⃣ Reviewing Test Results**
After a test run, all actions are logged in a text file:  
```plaintext
test_search_bar.txt
```
This contains:
- Each **action** taken (click, type, scroll, system).
- Any **user feedback** (accepted/rejected steps).
- Screenshots of each step for validation.

---

## **Features**
✅ **AI-based test execution** with **adaptive learning**  
✅ **User feedback integration** to refine AI decisions  
✅ **System navigation support** (Back, Home, Volume, Hide Keyboard)  
✅ **Smarter scrolling with dynamic buffer adjustments**  
✅ **Action logs for debugging & replaying tests (WIP)**  

---

## **Next Steps**
- 🚧 Improve AI predictions with **UI element tagging**  
- 🚧 Implement **automatic test replays**  
- 🚧 Add **error recovery & retries** for failed steps  

---

## **Demo**

https://drive.google.com/file/d/1hil-XaEwyV64rydFbNzpfxTxYqLoqp6w/preview 