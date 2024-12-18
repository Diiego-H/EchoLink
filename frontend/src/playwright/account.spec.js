import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser } from './utils/user.js';
import { test, expect } from '@playwright/test';

test('Edit Profile Successful', async ({ page }) => {
    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };


    // Register a new user
    await registerUser(userData.username, userData.email, userData.password);

    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(userData.email);
    await emailInput.press('Enter');

    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill(userData.password);
    await passwordInput.press('Enter');


    const successToast1 = page.locator('text="Log in successful!"');
    await expect(successToast1).toBeVisible();

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]'); // Update this selector as needed
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`); // Verify URL is correct

    // Start editing the profile
    const editButton = page.locator('[data-test="button-edit"]');
    await editButton.click();

    // Update profile fields
    await page.fill('[data-test="field-description"]', 'A new description about myself.');
    await page.fill('[data-test="field-genre"]', 'Jazz');

    // Save changes
    await editButton.click();

    // Verify success message
    const successToast = page.locator('text="Profile updated"');
    await expect(successToast).toBeVisible();

    // Verify changes are saved and visible
    await expect(page.locator('[data-test="field-description"]')).toHaveValue('A new description about myself.');
    await expect(page.locator('[data-test="field-genre"]')).toHaveValue('Jazz');
});

test('Delete Account Successful', async ({ page, context }) => {
    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    // Register a new user
    await registerUser(userData.username, userData.email, userData.password);

    // Log in with the new user
    await page.goto('/logIn');
    await page.fill('[data-test="field-email"]', userData.email);
    await page.fill('[data-test="field-password"]', userData.password);
    await page.press('[data-test="field-password"]', 'Enter');
    await expect(page).toHaveURL('/'); // Assuming the user is redirected to homepage

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]'); // Update this selector as needed
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`); // Verify URL is correct


    // Start editing the profile
    const editButton = page.locator('[data-test="button-edit"]');
    await editButton.click();

    // Click the delete account button
    const deleteButton = page.locator('[data-test="button-delete"]');
    await deleteButton.click();

    // Confirm account deletion in the confirmation dialog
    const confirmButton = page.locator('.swal2-confirm');
    await confirmButton.click();

    // Verify successful account deletion
    const deleteSuccessToast = page.locator('text="Deleted!"');
    await expect(deleteSuccessToast).toBeVisible();


    // Handle the SweetAlert confirmation
    const okButton = page.locator('.swal2-confirm'); // Assuming this is the OK button to close the alert
    await okButton.click();
    // Verify redirection to the homepage or logout page
    await expect(page).toHaveURL('/');

    // Check that the specific cookies are removed
    const cookies = await context.cookies();
    const authTokenCookie = cookies.find(cookie => cookie.name === 'auth_token');
    const loggedInCookie = cookies.find(cookie => cookie.name === 'logged_in');

    expect(authTokenCookie).toBeUndefined(); // auth_token should not exist
    expect(loggedInCookie).toBeUndefined(); // logged_in should not exist

    // Attempt to log in again with the deleted account
    await page.goto('/logIn');
    await page.fill('[data-test="field-email"]', userData.email);
    await page.fill('[data-test="field-password"]', userData.password);
    await page.press('[data-test="field-password"]', 'Enter');




    // Verify that a SweetAlert2 error popup appears with the appropriate message
    const errorPopup = page.locator('.swal2-popup .swal2-title');
    await expect(errorPopup).toHaveText('Log in failed');

    // Verify the specific error message
    const errorMessage = page.locator('.swal2-popup .swal2-html-container');
    await expect(errorMessage).toHaveText('Reason: The email is not associated to any account.');
});