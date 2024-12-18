import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser, registerArtist } from './utils/user.js';
import { test, expect } from '@playwright/test';

test('Follow and Unfollow an artist successfully', async ({ page }) => {

    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    const artistData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    // Register an artist
    await registerArtist(artistData.username, artistData.email, artistData.password);

    // Register a new user
    await registerUser(userData.username, userData.email, userData.password);

    // Log in the user
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(userData.email);
    await emailInput.press('Enter');

    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill(userData.password);
    await passwordInput.press('Enter');

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();


    // Redirect to the artist's page
    await page.goto(`/users/${artistData.username}`);
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Locate the follow button
    const followButton = page.locator('[data-test="button-follow"]');
    await expect(followButton).toBeVisible();

    // Click the follow button
    await followButton.click();

    // Verify the follow was successful
    const successToastFollow = page.locator('text="Follow successful!"');
    await expect(successToastFollow).toBeVisible();

    // Verify the follow button has changed the text to "Unfollow"
    await expect(followButton).toHaveText('Unfollow');

    // Click the follow button again
    await followButton.click();

    // Verify the unfollow was successful
    const successToastUnfollow = page.locator('text="Unfollow successful!"');
    await expect(successToastUnfollow).toBeVisible();
});

test('Non logged user cannot follow an artist', async ({ page }) => {

    const artistData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    // Register an artist
    await registerArtist(artistData.username, artistData.email, artistData.password);

    // Redirect to the artist's page
    await page.goto(`/users/${artistData.username}`);
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Try to locate the follow button and verify it is not visible
    const followButton = page.locator('[data-test="button-follow"]');
    await expect(followButton).not.toBeVisible();
});