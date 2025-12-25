import json
import sys
import os

# Add the current directory to the path so we can import the main module
sys.path.insert(0, os.path.dirname(__file__))

from main import handle_navigation

def test_navigation():
    """Test navigation callback for different user roles"""

    # Test cases: (button_id, user_data, expected_result)
    test_cases = [
        # Admin user should have access to all pages
        ("btn-dashboard", '{"role": "admin"}', "/dashboard"),
        ("btn-users", '{"role": "admin"}', "/dashboard/users"),
        ("btn-locations", '{"role": "admin"}', "/dashboard/locations"),
        ("btn-routes", '{"role": "admin"}', "/dashboard/routes"),
        ("btn-find-routes", '{"role": "admin"}', "/dashboard/find-routes"),
        ("btn-notifications", '{"role": "admin"}', "/dashboard/notifications"),

        # Student user should only have access to non-admin pages
        ("btn-dashboard", '{"role": "student"}', "/dashboard"),
        ("btn-find-routes", '{"role": "student"}', "/dashboard/find-routes"),

        # Student clicking admin buttons should return no_update (stay on current page)
        ("btn-users", '{"role": "student"}', "no_update"),
        ("btn-locations", '{"role": "student"}', "no_update"),
        ("btn-routes", '{"role": "student"}', "no_update"),
        ("btn-notifications", '{"role": "student"}', "no_update"),

        # Visitor and Staff should have same behavior as Student
        ("btn-users", '{"role": "visitor"}', "no_update"),
        ("btn-users", '{"role": "staff"}', "no_update"),
    ]

    print("Testing Navigation Logic...")
    print("=" * 50)

    all_passed = True

    for button_id, user_data, expected in test_cases:
        try:
            # Simulate callback context
            import dash
            ctx = type('MockContext', (), {
                'triggered': [{'prop_id': f'{button_id}.n_clicks'}] if button_id else []
            })()

            # Mock the callback context
            original_ctx = dash.callback_context
            dash.callback_context = ctx

            try:
                result = handle_navigation(
                    1 if button_id == "btn-dashboard" else None,  # dash_clicks
                    1 if button_id == "btn-users" else None,      # users_clicks
                    1 if button_id == "btn-locations" else None,  # locations_clicks
                    1 if button_id == "btn-routes" else None,     # routes_clicks
                    1 if button_id == "btn-find-routes" else None,# find_routes_clicks
                    1 if button_id == "btn-notifications" else None,# notifications_clicks
                    user_data
                )

                # Check result
                if expected == "no_update":
                    success = result == dash.no_update
                else:
                    success = result == expected

                status = "PASS" if success else "FAIL"
                if not success:
                    all_passed = False

                user_role = json.loads(user_data).get('role', 'unknown')
                print(f"{status}: {button_id} for {user_role} -> {result} (expected: {expected})")

            finally:
                dash.callback_context = original_ctx

        except Exception as e:
            print(f"ERROR: {button_id} - Exception: {e}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("All navigation tests PASSED! ✅")
    else:
        print("Some navigation tests FAILED! ❌")

    return all_passed

if __name__ == "__main__":
    test_navigation()