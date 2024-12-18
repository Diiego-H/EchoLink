import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import LogIn from '../pages/LogInDef.vue'

async function setFormValue(ref, value) {
    ref.setValue(value)
    await ref.trigger('submit')
}

describe('Log In Page Tests', () => {
    it('should validate fields', async () => {
        const wrapper = mount(LogIn)
        const email = wrapper.get('[data-test="field-email"]')
        const password = wrapper.get('[data-test="field-password"]')

        await setFormValue(email, 'invalidAdress')
        expect(wrapper.find('[data-test="field-email-warning"]').exists()).toBe(true) // Expect the warning element to be present

        await setFormValue(password, 'shortPW') // Too short
        expect(wrapper.find('[data-test="field-password-warning"]').exists()).toBe(true) // Expect the warning element to be present

        await setFormValue(password, 'longEnoughPW')
        expect(wrapper.find('[data-test="field-password-warning"]').exists()).toBe(false) // Expect no warning
    })
    it('should enable button on valid fields', async () => {
        const wrapper = mount(LogIn)
        const email = wrapper.get('[data-test="field-email"]')
        const password = wrapper.get('[data-test="field-password"]')
        const loginButton = wrapper.get('[data-test="button-login"]')

        await setFormValue(email, 'myemail@test.com')
        await setFormValue(password, 'shortPW') // Short password
        expect(loginButton.attributes().disabled).toBeDefined() // Button should disable

        await setFormValue(password, 'mypassword123') // Long password
        expect(loginButton.attributes().disabled).toBeUndefined() // Button should enable

        await setFormValue(email, 'invalidAdress') // Invalid email
        expect(loginButton.attributes().disabled).toBeDefined() // Button should disable
    })
})
