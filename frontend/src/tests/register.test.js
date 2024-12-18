import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import Register from '../pages/RegisterDef.vue'

async function setFormValue(ref, value) {
    ref.setValue(value)
    await ref.trigger('submit')
}

describe('Register Page Tests', () => {
    it('should validate fields', async () => {
        const wrapper = mount(Register)
        const username = wrapper.get('[data-test="field-username"]')
        const password = wrapper.get('[data-test="field-password"]')

        await setFormValue(username, 'with spaces')
        expect(wrapper.find('[data-test="field-username-warning"]').exists()).toBe(true) // Expect the warning element to be present

        await setFormValue(password, 'shortPW') // Too short
        expect(wrapper.find('[data-test="field-password-warning"]').exists()).toBe(true) // Expect the warning element to be present

        await setFormValue(password, 'longEnoughPW')
        expect(wrapper.find('[data-test="field-password-warning"]').exists()).toBe(false) // Expect no warning
    })

    it('should validate passwords match', async () => {
        const wrapper = mount(Register)
        const password = wrapper.get('[data-test="field-password"]')
        const passwordConfirmation = wrapper.get('[data-test="field-passwordconfirmation"]')

        await setFormValue(password, 'somepassword')
        await setFormValue(passwordConfirmation, 'someotherpassword')
        expect(wrapper.find('[data-test="field-passwordconfirmation-warning"]').exists()).toBe(true) // Expect the warning element to be present

        await setFormValue(password, 'someotherpassword')
        expect(wrapper.find('[data-test="field-passwordconfirmation-warning"]').exists()).toBe(false) // Expect no warning element
    })

    it('should enable button on valid fields', async () => {
        const wrapper = mount(Register)
        const email = wrapper.get('[data-test="field-email"]')
        const username = wrapper.get('[data-test="field-username"]')
        const password = wrapper.get('[data-test="field-password"]')
        const passwordConfirmation = wrapper.get('[data-test="field-passwordconfirmation"]')
        const tosCheckbox = wrapper.get('[data-test="checkbox-tos"]')
        const registerButton = wrapper.get('[data-test="button-register"]')

        await setFormValue(username, 'myusername')
        await setFormValue(email, 'myemail@test.com')
        await setFormValue(password, 'mypassword123')
        await setFormValue(passwordConfirmation, 'mypassword123')

        expect(registerButton.attributes().disabled).toBeDefined() // ToS not yet checked
        await setFormValue(tosCheckbox, true)
        expect(registerButton.attributes().disabled).toBeUndefined()
        
        await setFormValue(passwordConfirmation, 'otherPassword') // Password mismatch
        expect(registerButton.attributes().disabled).toBeDefined() // Button should disable again
    })
})