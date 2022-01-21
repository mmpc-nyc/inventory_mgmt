<template>
  <main>
    <form @submit.prevent="createCustomer">
      <section class="customer">
        <h2>Customer {{ customer.companyName }} {{ customer.firstName }} {{ customer.lastName }}</h2>
        <div>
          <input v-model="customer.firstName" placeholder="First Name">
          <input v-model="customer.lastName" placeholder="Last Name">
          <input v-model="customer.companyName" placeholder="Company Name">
        </div>

        <div class="contact">
          <h3>Customer Contact</h3>
          <input
              id="same-as-customer-name"
              v-model="customerContactSameAsCustomer"
              type="checkbox">
          <label for="same-as-customer-name">Same as Customer</label>
          <div>
            <input v-if="!customerContactSameAsCustomer" v-model="customer.contact.firstName" placeholder="First Name">
            <input v-else :value="customer.firstName" placeholder="First Name" disabled>
            <input v-if="!customerContactSameAsCustomer" v-model="customer.contact.lastName" placeholder="Last Name">
            <input v-else :value="customer.lastName" placeholder="Last Name" disabled>
            <input v-model="customer.contact.email" type="email" placeholder="Email">
            <input v-model="customer.contact.phone" type="tel" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}" placeholder="Phone">
          </div>
        </div>
      </section>


      <section class="service">
        <h2>Service</h2>
        <h3>Address</h3>
        <input v-model="serviceAddress.lineOne" placeholder="Address">
        <input v-model="serviceAddress.lineTwo" placeholder="Apt, Suite, etc..">

        <h3>Contact</h3>
        <input id="service-contact-same-as-customer-contact" v-model="serviceAddressContactSameAsCustomerContact"
               type="checkbox">
        <label for="service-contact-same-as-customer-contact">Same as Customer Contact</label>
        <div v-if="serviceAddressContactSameAsCustomerContact" class="service-address-contact">
          <input
              :value="customerContactSameAsCustomer ? customer.firstName : customer.contact.firstName"
              placeholder="First Name"
              disabled>
          <input
              :value="customerContactSameAsCustomer ?  customer.lastName : customer.contact.lastName"
              placeholder="Last Name"
              disabled>
          <input :value="customer.contact.email" disabled placeholder="Email">
          <input :value="customer.contact.phone" disabled placeholder="Phone">
        </div>
        <div v-else class="service-address-contact">
          <input v-model="serviceAddress.contact.firstName" placeholder="First Name">
          <input v-model="serviceAddress.contact.lastName" placeholder="Last Name">
          <input v-model="serviceAddress.contact.email" type="email" placeholder="Email">
          <input v-model="serviceAddress.contact.phone" type="tel" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
                 placeholder="Phone">
        </div>
      </section>

      <section class="billing">
        <h2>Billing</h2>
        <input id="same-as-service-address" v-model="billingAddressSameAsServiceAddress" type="checkbox">
        <label for="same-as-service-address">Same as Service Address</label>
        <h3>Address</h3>
        <div class="billing-address" v-if="!billingAddressSameAsServiceAddress">
          <input id="billing-address-line-1" v-model="billingAddress.lineOne" placeholder="Address">
          <input id="billing-address-line-2" v-model="billingAddress.lineTwo" placeholder="Apt, Suite, etc..">
        </div>
        <div class="billing-address" v-else>
          <input :value="serviceAddress.lineOne" placeholder="Address" disabled>
          <input :value="serviceAddress.lineTwo" placeholder="Apt, Suite, etc.." disabled>
        </div>
        <h3>Contact</h3>
        <input id="billing-contact-same-as-customer-contact" v-model="billingAddressContactSameAsCustomerContact"
               type="checkbox">
        <label for="billing-contact-same-as-customer-contact">Same as Customer Contact</label>

        <div v-if="billingAddressContactSameAsCustomerContact" class="service-address-contact">
          <input
              :value="customerContactSameAsCustomer ? customer.firstName : customer.contact.firstName"
              placeholder="First Name"
              disabled>
          <input
              :value="customerContactSameAsCustomer ?  customer.lastName : customer.contact.lastName"
              placeholder="Last Name"
              disabled>
          <input :value="customer.contact.email" disabled placeholder="Email">
          <input :value="customer.contact.phone" disabled placeholder="Phone">
        </div>
        <div v-else class="service-address-contact">
          <input v-model="billingAddress.contact.firstName" placeholder="First Name">
          <input v-model="billingAddress.contact.lastName" placeholder="Last Name">
          <input v-model="billingAddress.contact.email" type="email" placeholder="Email">
          <input v-model="billingAddress.contact.phone" type="tel" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}">
        </div>
      </section>

      <button type="submit">Submit</button>
    </form>
  </main>

</template>

<script>
export default {
  name: "CustomerAdminCreate",
  data() {
    return {
      customer: {
        firstName: "",
        lastName: "",
        companyName: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      serviceAddress: {
        lineOne: "",
        lineTwo: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      billingAddress: {

        lineOne: "",
        lineTwo: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      customerContactSameAsCustomer: true,
      serviceAddressContactSameAsCustomerContact: true,
      billingAddressSameAsServiceAddress: true,
      billingAddressContactSameAsCustomerContact: true,
      billingAddressContactSameAsServiceAddressContact: true,
    }
  },
  methods: {
    createCustomer() {
      console.log("Create Customer")
    },
  },
}
</script>

<style scoped lang="scss">
@import "/scss/variables";

section {
  padding: 1rem;
  @include shadow-1;
}
</style>