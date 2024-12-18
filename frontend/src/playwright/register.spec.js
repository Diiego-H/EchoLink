import { test, expect } from '@playwright/test';
import  {generateRandomEmail, generateRandomPassword, generateRandomUsername} from './utils/dataGenerator.js';

const email = generateRandomEmail();
const password = generateRandomPassword();
const username = generateRandomUsername();

export const registerData = {
    valid: {
        username: username,
        email: email,
        password: password,
        confirmPassword: password,
    },
    invalidEmail: {
        username: username,
        email: 'invalidemail',
        password: password,
        confirmPassword: password,
    },
    mismatchedPasswords: {
        username: username,
        email: email,
        password: password,
        confirmPassword: generateRandomPassword(),
    },
};


test('Successful registration', async ({ page }) => {
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Fill in valid user data
    const { username, email, password, confirmPassword } = registerData.valid;
    await page.locator('[data-test="field-username"]').fill(username);
    await page.locator('[data-test="field-email"]').fill(email);
    await page.locator('[data-test="field-password"]').fill(password);
    await page.locator('[data-test="field-passwordconfirmation"]').fill(confirmPassword);
    await page.locator('[data-test="checkbox-tos"]').check();

    // Submit the form
    await page.locator('[data-test="button-register"]').click();

    // Verify successful registration
    const successToast = page.locator('text="Registration successful!"');
    await expect(successToast).toBeVisible();
    await expect(page).toHaveURL('/'); // Redirect to homepage
});

// Register a user as an artist
test('Successful registration as an artist', async ({ page }) => {
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Determine the user data
    const username = generateRandomUsername();
    const email = generateRandomEmail();
    const password = generateRandomPassword();
    
    // Fill in valid artist data
    await page.locator('[data-test="field-username"]').fill(username);
    await page.locator('[data-test="field-email"]').fill(email);
    await page.locator('[data-test="field-password"]').fill(password);
    await page.locator('[data-test="field-passwordconfirmation"]').fill(password);
    
    // Locate the dropdown and select the artist option
    await page.locator('[data-test="field-role"]').selectOption('Artist');

    // Check the TOS checkbox
    await page.locator('[data-test="checkbox-tos"]').check();

    // Submit the form
    await page.locator('[data-test="button-register"]').click();

    // Verify successful registration
    const successToast = page.locator('text="Registration successful!"');
    await expect(successToast).toBeVisible();
    await expect(page).toHaveURL('/'); // Redirect to homepage
});


test('Registration fails with invalid email', async ({ page }) => {
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Fill in invalid email data
    const { username, email, password, confirmPassword } = registerData.invalidEmail;
    await page.locator('[data-test="field-username"]').fill(username);
    await page.locator('[data-test="field-email"]').fill(email);
    await page.locator('[data-test="field-password"]').fill(password);
    await page.locator('[data-test="field-passwordconfirmation"]').fill(confirmPassword);
    await page.locator('[data-test="checkbox-tos"]').check();

    // Verify error message for invalid email
    const emailWarning = page.locator('text="Must be a valid address"');
    await expect(emailWarning).toBeVisible();
});

test('Registration fails with mismatched passwords', async ({ page }) => {
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Fill in data with mismatched passwords
    const { username, email, password, confirmPassword } = registerData.mismatchedPasswords;
    await page.locator('[data-test="field-username"]').fill(username);
    await page.locator('[data-test="field-email"]').fill(email);
    await page.locator('[data-test="field-password"]').fill(password);
    await page.locator('[data-test="field-passwordconfirmation"]').fill(confirmPassword);
    await page.locator('[data-test="checkbox-tos"]').check();

    // Verify error message for mismatched passwords
    const confirmPasswordWarning = page.locator('text="Passwords must match"');
    await expect(confirmPasswordWarning).toBeVisible();
});
