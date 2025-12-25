import json
import sys
import os

# Add the current directory to the path so we can import the main module
sys.path.insert(0, os.path.dirname(__file__))

def test_navigation_login_page():
    """Test that navigation callback doesn't cause errors when user is not logged in"""

    # Import after setting path
    from main import handle_navigation
    import dash

    print("Testing Navigation Callback on Login Page...")
    print("=" * 50)

    # Test case: User not logged in (None user_data)
    try:
        # Mock callback context for btn-dashboard click
        ctx = type('MockContext', (), {
            'triggered': [{'prop_id': 'btn-dashboard.n_clicks'}]
        })()

        # Mock the callback context
        original_ctx = dash.callback_context
        dash.callback_context = ctx

        try:
            result = handle_navigation(
                1,  # dash_clicks
                None, None, None, None, None,  # other button clicks
                None  # user_data (not logged in)
            )

            # Should return no_update when user is not logged in
            success = result == dash.no_update
            status = "PASS" if success else "FAIL"

            print(f"{status}: Navigation with no user logged in -> {result}")

            return success

        finally:
            dash.callback_context = original_ctx

    except Exception as e:
        print(f"ERROR: Exception occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_navigation_login_page()
    print("=" * 50)
    if success:
        print("✅ Navigation test PASSED - No errors on login page!")
    else:
        print("❌ Navigation test FAILED")