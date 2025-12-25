import json
import sys
import os

# Add the current directory to the path so we can import the main module
sys.path.insert(0, os.path.dirname(__file__))

from main import router

def test_role_based_access():
    """Test role-based access control in the router"""

    # Test user data
    admin_user = {'role': 'admin', 'username': 'admin'}
    regular_user = {'role': 'user', 'username': 'student'}

    # Convert to JSON strings as they would be in the app
    admin_data = json.dumps(admin_user)
    user_data = json.dumps(regular_user)

    # Test cases: (pathname, user_data, expected_access)
    test_cases = [
        # Admin should have access to all pages
        ('/dashboard/users', admin_data, True),
        ('/dashboard/locations', admin_data, True),
        ('/dashboard/routes', admin_data, True),
        ('/dashboard/reports', admin_data, True),
        ('/dashboard/notifications', admin_data, True),
        ('/dashboard/find-routes', admin_data, True),

        # Regular user should be denied access to admin pages
        ('/dashboard/users', user_data, False),
        ('/dashboard/locations', user_data, False),
        ('/dashboard/routes', user_data, False),
        ('/dashboard/reports', user_data, False),

        # Regular user should have access to notifications (view only, actions disabled)
        ('/dashboard/notifications', user_data, True),

        # Regular user should have access to public pages
        ('/dashboard/find-routes', user_data, True),
        ('/dashboard', user_data, True),
    ]

    print("Testing Role-Based Access Control...")
    print("=" * 50)

    all_passed = True

    for pathname, user_data, should_have_access in test_cases:
        try:
            result = router(pathname, user_data)

            # Check if access was granted or denied
            # For denied access, the result should contain an Alert component with "Access Denied"
            result_str = str(result)
            has_access_denied = "Access Denied" in result_str

            if should_have_access:
                # Should NOT have access denied message
                has_access = not has_access_denied
            else:
                # Should HAVE access denied message
                has_access = has_access_denied

            status = "PASS" if has_access else "FAIL"
            if not has_access:
                all_passed = False

            user_type = 'admin' if 'admin' in user_data else 'user'
            expected = 'granted' if should_have_access else 'denied'
            actual = 'granted' if not has_access_denied else 'denied'

            print(f"{status}: {pathname} for {user_type} - expected {expected}, got {actual}")

        except Exception as e:
            print(f"ERROR: {pathname} - Exception: {e}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("All tests PASSED! Role-based access control is working correctly.")
    else:
        print("Some tests FAILED! Please check the implementation.")

    return all_passed

if __name__ == "__main__":
    test_role_based_access()