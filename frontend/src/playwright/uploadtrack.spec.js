import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerArtist } from './utils/user.js';
import { test, expect } from '@playwright/test';

test('Create and Delete  Successful', async ({ page }) => {

    // Generate random user data
    const artistData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    // Register an artist
    await registerArtist(artistData.username, artistData.email, artistData.password);

    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(artistData.email);
    await emailInput.press('Enter');

    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill(artistData.password);
    await passwordInput.press('Enter');

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]');
    await expect(profileButton).toBeVisible();
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Redirect to dummy 
    await page.goto('/');
    await expect(page).toHaveURL('/');


    // Access the "Artist Settings" dropdown
    const artistSettingsDropdown = page.locator('[data-test="artist-menu"]');
    await artistSettingsDropdown.click(); // Open the dropdown

    // Click on "Upload Track"
    const uploadTrackLink = page.locator('[data-test="upload-track-laptop"]');
    await uploadTrackLink.click(); // Click the "Upload Track" link

    // Verify navigation to the "Upload Track" page
    await expect(page).toHaveURL(/\/uploadTrack/); // Ensure the URL contains "/uploadTrack"

    // Locate the fields
    const titleInput = page.locator('[data-test="field-title"]');
    await expect(titleInput).toBeVisible();
    await titleInput.fill("Test Title");

    const descriptionInput = page.locator('[data-test="field-album"]');
    await expect(descriptionInput).toBeVisible();
    await descriptionInput.fill("Test Description");

    const genreInput = page.locator('[data-test="field-genre"]');
    await expect(genreInput).toBeVisible();
    await genreInput.fill("Pop");

    const releasedateInput = page.locator('[data-test="field-release-date"]');
    await expect(releasedateInput).toBeVisible();
    await releasedateInput.fill("2024-11-30");

    // Locate the upload button
    const uploadButton = page.locator('[data-test="button-uploadTrack"]');
    await expect(uploadButton).toBeVisible();
    await uploadButton.click();

    // Locate the success toast
    const successUpload = page.locator('text="Track uploaded successfully!"');
    await expect(successUpload).toBeVisible();

});
