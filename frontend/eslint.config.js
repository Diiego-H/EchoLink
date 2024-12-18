import vue from 'eslint-plugin-vue';
import vueEslintParser from 'vue-eslint-parser';

export default [
  {
    files: ['**/*.js', '**/*.vue'],
    ignores: ['dist/**', 'src/tests/**', 'src/assets/**'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: vueEslintParser,
    },
    plugins: {
      vue,
    },
    rules: {
      'eqeqeq': 'error', // Enforce strict equality
      'no-unused-vars': 'warn', // Warn about unused variables
      'no-undef': 'off', // Disable no-undef to allow global variables
      'quotes': ['off', 'single'], // Disable quotes rule to allow any quote style
      'no-var': 'error', // Disallow var, use let or const instead
      'prefer-const': 'error', // Prefer const over let for variables that are never reassigned
      'vue/no-unused-components': 'warn', // Warn about unused Vue components
      'vue/require-prop-types': 'error', // Require prop types in Vue components
      'vue/multi-word-component-names': ['error', {
        // This option enforces multi-word component names
        'ignores': ['App'], // You can add exceptions here if needed
      }],
    },
  },
];