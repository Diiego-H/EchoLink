import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser, registerArtist } from './utils/user.js';
import { test, expect } from '@playwright/test';

test('Ask artist not following error', async ({ page }) => {

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

    // Locate the Ask me something button data-test="button-ask"
    const askButton = page.locator('[data-test="button-ask"]');
    await expect(askButton).toBeVisible();

    // Click the ask button
    await askButton.click();

    // Verify the follow was unsuccessful
    const errorToast = page.locator('text="You need to follow the artist to send them questions"');
    await expect(errorToast).toBeVisible();

    // Verify the follow button
    const followButton = page.locator('[data-test="button-follow"]');
    await expect(followButton).toBeVisible();
    await expect(followButton).toHaveText('Follow');

});

test('Ask a question to an artist and reject it', async ({ page }) => {

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

    // Locate the Ask me something button data-test="button-ask"
    const askButton = page.locator('[data-test="button-ask"]');
    await expect(askButton).toBeVisible();

    // Click the ask button
    await askButton.click();

    // Locate the input field
    const textarea = page.locator('textarea[id="swal-input"]');
    await expect(textarea).toBeVisible();
    await textarea.fill('Hello, how are you?');

    // Locate the Send button
    const sendButton = page.locator('button:has-text("Send")');
    await expect(sendButton).toBeVisible();
    await sendButton.click();

    // Verify the question was sent
    const successToastQuestion = page.locator('text="Your question has been sent successfully!"');
    await expect(successToastQuestion).toBeVisible();

    //##############################################
    // Log in as the artist and reject the question
    //##############################################

    // Log out the user
    const logoutButton = page.locator('[data-test="logout-laptop"]');
    await expect(logoutButton).toBeVisible();
    await logoutButton.click();

    // Log in the artist
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    await emailInput.fill(artistData.email);
    await emailInput.press('Enter');

    await passwordInput.fill(artistData.password);
    await passwordInput.press('Enter');

    await expect(successToast).toBeVisible();

    // Redirect to the dashboard page
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/dashboard');

    // Locate the question
    const questionDiv = page.locator('div.question.relative.group');
    await expect(questionDiv).toBeVisible();
    await questionDiv.hover();

    // Locate the answer button
    const answerButton = page.locator('button:has-text("Answer")').nth(1);
    await expect(answerButton).toBeVisible();
    await answerButton.click();

    // Locate the Reject button
    const rejectButton = page.locator('button:has-text("Reject Question")');
    await expect(rejectButton).toBeVisible();

    // Click the Reject button
    await rejectButton.click();

    // Locate the confirmation button
    const yesButton = page.locator('button:has-text("Yes, reject it ")');
    await expect(yesButton).toBeVisible();

    // Click the Yes button
    await yesButton.click();

    // Verify the question was rejected
    const successToastReject = page.locator('text="The question has been rejected."');
    await expect(successToastReject).toBeVisible();
});

test('Ask a question to an artist and respond it', async ({ page }) => {

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

    // Locate the Ask me something button data-test="button-ask"
    const askButton = page.locator('[data-test="button-ask"]');
    await expect(askButton).toBeVisible();

    // Click the ask button
    await askButton.click();

    // Locate the input field
    const textarea = page.locator('textarea[id="swal-input"]');
    await expect(textarea).toBeVisible();
    await textarea.fill('Hello, how are you?');

    // Locate the Send button
    const sendButton = page.locator('button:has-text("Send")');
    await expect(sendButton).toBeVisible();
    await sendButton.click();

    // Verify the question was sent
    const successToastQuestion = page.locator('text="Your question has been sent successfully!"');
    await expect(successToastQuestion).toBeVisible();

    //##############################################
    // Log in as the artist and answer the question
    //##############################################

    // Log out the user
    const logoutButton = page.locator('[data-test="logout-laptop"]');
    await expect(logoutButton).toBeVisible();
    await logoutButton.click();

    // Log in the artist
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    await emailInput.fill(artistData.email);
    await emailInput.press('Enter');

    await passwordInput.fill(artistData.password);
    await passwordInput.press('Enter');

    await expect(successToast).toBeVisible();

    // Redirect to the dashboard page
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/dashboard');

    // Locate the question
    const questionDiv = page.locator('div.question.relative.group');
    await expect(questionDiv).toBeVisible();
    await questionDiv.hover();

    // Locate the answer button
    const answerButton = page.locator('button:has-text("Answer")').nth(1);
    await expect(answerButton).toBeVisible();
    await answerButton.click();

    // Locate the fields
    const answerInput = page.locator('textarea[id="swal-input"]');
    await expect(answerInput).toBeVisible();
    await answerInput.fill('I am fine, thank you!');

    // Locate the Send button
    const sendResponseButton = page.locator('button:has-text("Send Response")');
    await expect(sendResponseButton).toBeVisible();
    await sendResponseButton.click();

    // Locate the success toast
    const successToastAnswer = page.locator('text="Your response has been sent successfully!"');
    await expect(successToastAnswer).toBeVisible();
    
});