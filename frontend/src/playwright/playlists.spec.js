import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser } from './utils/user.js';
import { test, expect } from '@playwright/test';


test('Create and Delete Playlist Successful', async ({ page }) => {

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

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]');
    await expect(profileButton).toBeVisible();
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`);

    // Click the "Add New Playlist" button
    const btnAddPlaylist = page.locator('button:has-text("Add New Playlist")');
    await expect(btnAddPlaylist).toBeVisible();
    await btnAddPlaylist.click();

    // Check the URL is correct
    await expect(page).toHaveURL('/playlists/new');

    // Fill out the form
    const playlistName = page.locator('input[data-v-c92f29ec]');
    await expect(playlistName).toBeVisible();
    await playlistName.fill('My New Playlist');

    const playlistDescription = page.locator('textarea[data-v-c92f29ec]');
    await expect(playlistDescription).toBeVisible();
    await playlistDescription.fill('This is a new playlist.');

    // Create the form
    const btnCreate = page.locator('button:has-text("Create")');
    await expect(btnCreate).toBeVisible();
    await btnCreate.click();

    const btnshare = page.locator('button:has-text("Share")');
    await expect(btnshare).toBeVisible();

    // Get the playlist ID from the URL
    const url = page.url();
    const playlistId = url.split('/').pop();

    // Redirect to dummy page
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // Redirect to the playlist page
    await page.goto(`/playlists/${playlistId}`);
    await expect(page).toHaveURL(`/playlists/${playlistId}`);

    // Check url is correct
    const btnEdit = page.locator('button:has-text("Edit")');
    await expect(btnEdit).toBeVisible();

    // Redirect again to /users/username
    await page.goto(`/users/${userData.username}`);
    await expect(page).toHaveURL(`/users/${userData.username}`);

    const playlistLink = await page.locator('a', { hasText: 'My New Playlist' });
    await expect(playlistLink).toHaveAttribute('href', '/playlists/' + playlistId); 
    await expect(playlistLink).toBeVisible();

    // Delete the playlist
    const relatedButton = page.locator(`xpath=//a[@href="/playlists/${playlistId}"]/ancestor::div//button[contains(@class, "btn-delete")]`);    // Verificar que el botón está visible
    await expect(relatedButton).toBeVisible();
    await relatedButton.click();

    // Confirm the deletion
    const btnDelete = page.locator('button:has-text("OK")');
    await expect(btnDelete).toBeVisible();
    await btnDelete.click();

    // Check the playlist is no longer visible
    await expect(playlistLink).not.toBeVisible(); 
    await expect(playlistLink).toHaveCount(0); 
});

test('Create Private Playlist', async ({ page }) => {

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

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]');
    await expect(profileButton).toBeVisible();
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`);

    // Click the "Add New Playlist" button
    const btnAddPlaylist = page.locator('button:has-text("Add New Playlist")');
    await expect(btnAddPlaylist).toBeVisible();
    await btnAddPlaylist.click();

    // Check the URL is correct
    await expect(page).toHaveURL('/playlists/new');

    // Fill out the form
    const playlistName = page.locator('input[data-v-c92f29ec]');
    await expect(playlistName).toBeVisible();
    await playlistName.fill('My New Playlist');

    const playlistDescription = page.locator('textarea[data-v-c92f29ec]');
    await expect(playlistDescription).toBeVisible();
    await playlistDescription.fill('This is a new playlist.');

    const visibilityDropdown = page.locator('.multiselect__single');
    await visibilityDropdown.click();
    const privateOption = page.locator('text=Private');
    await expect(privateOption).toBeVisible();
    await privateOption.click();

    // Verify the value is "Private"
    await expect(visibilityDropdown).toHaveText('Private');

    // Create the form
    const btnCreate = page.locator('button:has-text("Create")');
    await expect(btnCreate).toBeVisible();
    await btnCreate.click();

    const btnshare = page.locator('button:has-text("Share")');
    await expect(btnshare).toBeVisible();

    // Get the playlist ID from the URL
    const url = page.url();
    const playlistId = url.split('/').pop();

    // Redirect to dummy page
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // Locate the button Log Out
    const btnLogOut = page.locator('[data-test="logout-laptop"]');
    await expect(btnLogOut).toBeVisible();
    await btnLogOut.click();

    // Redirect to register page
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Register a new user
    const userData2 = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    await registerUser(userData2.username, userData2.email, userData2.password);

    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput2 = page.locator('[data-test="field-email"]');
    await emailInput2.fill(userData2.email);
    await emailInput2.press('Enter');

    const passwordInput2 = page.locator('[data-test="field-password"]');
    await passwordInput2.fill(userData2.password);
    await passwordInput2.press('Enter');

    const successToast2 = page.locator('text="Log in successful!"');
    await expect(successToast2).toBeVisible();

    // Redirect to the playlist page
    await page.goto(`/playlists/${playlistId}`);
    await expect(page).toHaveURL(`/playlists/${playlistId}`);

    // Check url is correct. should have an error
    const parentDiv = page.locator('div');

    // Localiza el enlace <a> dentro del div con el texto 'Return to homepage'
    const returnLink = parentDiv.locator('a', { hasText: 'Return to homepage' });

    // Verificar que el enlace es visible
    await expect(returnLink).toBeVisible();

    // Hacer clic en el enlace
    await returnLink.click();

    // Verificar que la URL es correcta
    await expect(page).toHaveURL('/');

});

test('Create Public Playlist', async ({ page }) => {

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

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]');
    await expect(profileButton).toBeVisible();
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`);

    // Click the "Add New Playlist" button
    const btnAddPlaylist = page.locator('button:has-text("Add New Playlist")');
    await expect(btnAddPlaylist).toBeVisible();
    await btnAddPlaylist.click();

    // Check the URL is correct
    await expect(page).toHaveURL('/playlists/new');

    // Fill out the form
    const playlistName = page.locator('input[data-v-c92f29ec]');
    await expect(playlistName).toBeVisible();
    await playlistName.fill('My New Playlist');

    const playlistDescription = page.locator('textarea[data-v-c92f29ec]');
    await expect(playlistDescription).toBeVisible();
    await playlistDescription.fill('This is a new playlist.');

    // Create the form
    const btnCreate = page.locator('button:has-text("Create")');
    await expect(btnCreate).toBeVisible();
    await btnCreate.click();

    const btnshare = page.locator('button:has-text("Share")');
    await expect(btnshare).toBeVisible();

    // Get the playlist ID from the URL
    const url = page.url();
    const playlistId = url.split('/').pop();

    // Redirect to dummy page
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // Locate the button Log Out
    const btnLogOut = page.locator('[data-test="logout-laptop"]');
    await expect(btnLogOut).toBeVisible();
    await btnLogOut.click();

    // Redirect to register page
    await page.goto('/register');
    await expect(page).toHaveURL('/register');

    // Register a new user
    const userData2 = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    await registerUser(userData2.username, userData2.email, userData2.password);

    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput2 = page.locator('[data-test="field-email"]');
    await emailInput2.fill(userData2.email);
    await emailInput2.press('Enter');

    const passwordInput2 = page.locator('[data-test="field-password"]');
    await passwordInput2.fill(userData2.password);
    await passwordInput2.press('Enter');

    // Redirect to the playlist page
    await page.goto(`/playlists/${playlistId}`);
    await expect(page).toHaveURL(`/playlists/${playlistId}`);

    const btnShare = page.locator('button:has-text("Share")');
    await expect(btnShare).toBeVisible();
});

