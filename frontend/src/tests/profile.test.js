import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import Profile from '../pages/ProfileDef.vue'
import { ref, reactive, nextTick } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import UserService from '../services/user.js'
import PlaylistService from '../services/playlist.js'

const USERNAME = "Pip"
const DESCRIPTION = "Test desc"
const GENRE = "Test genre"
const VISIBILITY = "public"
// Mock API response
const USER_DATA = {
    username: USERNAME,
    description: DESCRIPTION,
    genre: GENRE,
    visibility: VISIBILITY,
    role: 'listener',
}

const mockRouter = createRouter({ history: createWebHistory(), routes: [] });
mockRouter.currentRoute.value.params = {
    username: USERNAME
};

describe('When profile is accessed', () => {
    it('should show user data', async () => {
        // TODO setup some mocking library instead
        UserService.get = function() {
            return USER_DATA
        }
        UserService.isLoggedIn = function() {
            return true
        }
        UserService.getCurrentUsername = function() {
            return USERNAME
        }
        PlaylistService.getUserPlaylists = function() {
            return new Array()
        }

        const wrapper = mount(Profile, {
            global: {
                plugins: [mockRouter],
            }
        })

        // Wait for both user and loaded ref updates to resolve
        await nextTick()
        await nextTick()

        const username = wrapper.find('[data-test="label-username"]')
        const editButton = wrapper.find('[data-test="button-edit"]')
        const visibilityBadge = wrapper.find('[data-test="badge-visibility"]')
        const description = wrapper.find('[data-test="field-description"]')
        const genre = wrapper.find('[data-test="field-genre"]')
        const errorContainer = wrapper.find('[data-test="container-error"]')

        expect(errorContainer.exists()).toBe(false)

        // Expect all fields to be properly filled in
        expect(username.text()).toBe(USERNAME)
        expect(description.element.value).toBe(DESCRIPTION)
        expect(genre.element.value).toBe(GENRE)

        // Expect profile edition elements to exist
        expect(visibilityBadge.exists()).toBe(true)
        expect(editButton.exists()).toBe(true)

        // Expect fields to be not editable
        expect(description.attributes().readonly).toBeDefined()
        expect(genre.attributes().readonly).toBeDefined()
    })
    it('should allow editing', async () => {
        // TODO setup some mocking library instead
        UserService.get = function() {
            return USER_DATA
        }
        UserService.isLoggedIn = function() {
            return true
        }
        UserService.getCurrentUsername = function() {
            return USERNAME
        }
        PlaylistService.getUserPlaylists = function() {
            return new Array()
        }

        const wrapper = mount(Profile, {
            global: {
                plugins: [mockRouter],
            }
        })

        // Wait for both user and loaded ref updates to resolve
        await nextTick()
        await nextTick()

        const username = wrapper.find('[data-test="label-username"]')
        const editButton = wrapper.find('[data-test="button-edit"]')
        const visibilityBadge = wrapper.find('[data-test="badge-visibility"]')
        const description = wrapper.find('[data-test="field-description"]')
        const genre = wrapper.find('[data-test="field-genre"]')
        const errorContainer = wrapper.find('[data-test="container-error"]')

        expect(errorContainer.exists()).toBe(false)

        // Expect all fields to be properly filled in
        expect(username.text()).toBe(USERNAME)
        expect(description.element.value).toBe(DESCRIPTION)
        expect(genre.element.value).toBe(GENRE)

        // Expect profile edition elements to exist
        expect(visibilityBadge.exists()).toBe(true)
        expect(editButton.exists()).toBe(true)
        await editButton.trigger('click')

        // Expect fields to be editable
        expect(description.attributes().readonly).toBeUndefined()
        expect(genre.attributes().readonly).toBeUndefined()
    })
    it('should not show editing options when logged out', async () => {
        // TODO setup some mocking library instead
        UserService.get = function() {
            return USER_DATA
        }
        UserService.isLoggedIn = function() {
            return false
        }
        UserService.getCurrentUsername = function() {
            return null
        }
        PlaylistService.getUserPlaylists = function() {
            return new Array()
        }

        const wrapper = mount(Profile, {
            global: {
                plugins: [mockRouter],
            }
        })

        // Wait for both user and loaded ref updates to resolve
        await nextTick()
        await nextTick()

        const editButton = wrapper.find('[data-test="button-edit"]')
        const visibilityBadge = wrapper.find('[data-test="badge-visibility"]')
        const errorContainer = wrapper.find('[data-test="container-error"]')

        expect(errorContainer.exists()).toBe(false)

        // Expect profile edition elements to not exist
        expect(visibilityBadge.exists()).toBe(false)
        expect(editButton.exists()).toBe(false)
    })
})

describe('When a profile page fails to load', () => {
    it('should show error message', async () => {
        // TODO setup some mocking library instead
        UserService.get = function() {
            throw {
                response: {
                    data: {
                        detail: 'User not found'
                    }
                }
            }
        }

        const wrapper = mount(Profile, {
            global: {
                plugins: [mockRouter],
            }
        })

        // Wait for both user and loaded ref updates to resolve
        await nextTick()
        await nextTick()

        const mainContainer = wrapper.find('[data-test="container-main"]')
        const errorContainer = wrapper.find('[data-test="container-error"]')

        // Expect no profile data to be shown
        expect(errorContainer.exists()).toBe(true)
        expect(mainContainer.exists()).toBe(false)
    })
})