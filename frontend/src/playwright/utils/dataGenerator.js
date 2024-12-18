/**
 * Generates a random username.
 * The username consists of 6-12 characters (letters, digits, underscores).
 */
export function generateRandomUsername() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_';
    const length = Math.floor(Math.random() * 7) + 6; // Random length between 6 and 12
    return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

/**
 * Generates a random password.
 * The password consists of 8-16 characters including letters, digits, and special characters.
 */
export function generateRandomPassword() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+';
    const length = Math.floor(Math.random() * 9) + 8; // Random length between 8 and 16
    return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

/**
 * Generates a random email address.
 * The email consists of a random username, a random domain name, and a TLD.
 */
export function generateRandomEmail() {
    const domains = ['example', 'test', 'random', 'mail'];
    const tlds = ['com', 'org', 'net', 'io'];
    const username = generateRandomUsername();
    const domain = domains[Math.floor(Math.random() * domains.length)];
    const tld = tlds[Math.floor(Math.random() * tlds.length)];
    return `${username}@${domain}.${tld}`;
}
