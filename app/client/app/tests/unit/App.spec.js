import { expect } from 'chai'
import { shallowMount } from '@vue/test-utils'
import App from '@/App.vue'

describe('App.vue', () => {
  it('renders App', () => {
    const msg = 'Sending an email'
    const title = 'Sending an email via APIs'
    const wrapper = shallowMount(App)
    const mydiv = wrapper.find(App)
    console.log('=========================')
    console.log(wrapper.html())
    console.log(mydiv)
    console.log(wrapper.props())
    for (let i in mydiv) {
      console.log(i)
    }
    expect(wrapper.text()).to.include(msg)
    expect(wrapper.html()).to.include(title)
    expect(wrapper.contains('div')).to.equal(true)
    expect(wrapper.contains('el-form')).to.equal(true)
    expect(wrapper.contains('el-form-item')).to.equal(true)
    expect(wrapper.contains('el-button')).to.equal(true)
    expect(wrapper.contains('el-input')).to.equal(true)
  })
})
