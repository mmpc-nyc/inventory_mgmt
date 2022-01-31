<template>
  <ui-form type="|" item-margin-bottom="16" action-align="center">
    <template #default="{ actionClass }">
      <ui-card>
        <!-- Customer Section -->
        <ui-card class="customer">
          <ui-card-text><h2 :class="[$tt('headline4')]">Customer {{ customer.name() }}</h2>
          </ui-card-text>
          <ui-textfield required v-model="customer.first_name">
            {{ validMsg.first_name ? validMsg.first_name : "First Name" }}
          </ui-textfield>
          <ui-textfield required v-model="customer.last_name">{{
              validMsg.last_name ? validMsg.last_name : "Last Name"
            }}
          </ui-textfield>
          <ui-textfield v-model="customer.company_name">Company Name</ui-textfield>

          <ui-textfield required v-model="customer.email" type="email">
            {{ validMsg.email ? validMsg.email : "Email" }}
            <template #after>
              <ui-textfield-icon>email</ui-textfield-icon>
            </template>
          </ui-textfield>
          <ui-textfield required helper-text-id="customer-phone-number-helper-text" v-model="customer.phone_number"
                        pattern="\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$" type="tel">
            {{ validMsg.phone_number ? validMsg.phone_number : "Phone Number" }}
            <template #after>
              <ui-textfield-icon>phone</ui-textfield-icon>
            </template>
          </ui-textfield>
        </ui-card>

        <!-- Service Location Section -->
        <ui-card class="service-locations">
          <ui-card-text><h2 :class="$tt('headline4')">Service Location(s)</h2></ui-card-text>
          <div v-for="(location, index) in customer.service_locations" :service_location="location"
               :key="index" class="location">
            <div class="location-inputs">
              <google-map-auto-complete :class="`location-address-line-1`" :location="location"
                                        @setLocation="setLocation"></google-map-auto-complete>
              <ui-textfield :class="`location-address-line-2`" v-model="location.address_line_2">Apt, Ste, etc...
              </ui-textfield>
              <ui-textfield required disabled :class="`location-city`" v-model="location.city">City</ui-textfield>
              <ui-textfield required disabled :class="`location-state`" v-model="location.state">State</ui-textfield>
              <ui-textfield required disabled :class="`location-postal-code`" v-model="location.postal_code">Postal
                Code
              </ui-textfield>
            </div>
            <google-map :class="`location-map`" :location="location"></google-map>
            <ui-divider :class="`location-divider`">
              <ui-form-field>
                <ui-checkbox :input-id="`service-contact-same-as-customer-contact-${index}`"
                             v-model="location.contact_same_as_customer"
                             type="checkbox"></ui-checkbox>
                <label :for="`service-contact-same-as-customer-contact-${index}`">Contact Same as Customer</label>
              </ui-form-field>
            </ui-divider>
            <div :class="`location-contacts`" v-if="!location.contact_same_as_customer">
              <h3 :class="$tt('headline5')">Contact(s)</h3>
              <div class="contact" v-for="(contact, index) in location.contacts" :key="index" :contact="contact">
                <ui-textfield v-model="contact.first_name">First Name</ui-textfield>
                <ui-textfield v-model="contact.last_name">Last Name</ui-textfield>
                <ui-textfield v-model="contact.emails[0]" type="email">Email
                  <template #after>
                    <ui-textfield-icon>email</ui-textfield-icon>
                  </template>
                </ui-textfield>
                <ui-textfield v-model="location.contacts.phone_numbers[0]"
                              pattern="\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$" type="tel"
                >Phone
                  <template #after>
                    <ui-textfield-icon>phone</ui-textfield-icon>
                  </template>
                </ui-textfield>
              </div>
            </div>
          </div>
        </ui-card>

        <ui-card class="billing-location">
          <ui-card-text>
            <h2 :class="$tt('headline4')">Billing Location
              <ui-form-field>
                <ui-checkbox input-id="same-as-service-address"
                             v-model="billing_location_same_as_service_location"
                             type="checkbox"></ui-checkbox>
                <label for="same-as-service-address">Same as Service Location</label>
              </ui-form-field>
            </h2>
          </ui-card-text>
          <div class="location" v-if="!billing_location_same_as_service_location">
            <div class="location-inputs">
              <google-map-auto-complete :class="`location-address-line-1`" :location="customer.billing_location"
                                        @setLocation="setLocation"></google-map-auto-complete>
              <ui-textfield :class="`location-address-line-2`" v-model="customer.billing_location.address_line_2">Apt,
                Ste, etc...
              </ui-textfield>
              <ui-textfield disabled required :class="`location-city`" v-model="customer.billing_location.city">City
              </ui-textfield>
              <ui-textfield disabled required :class="`location-state`" v-model="customer.billing_location.state">
                State
              </ui-textfield>
              <ui-textfield disabled required :class="`location-postal-code`"
                            v-model="customer.billing_location.postal_code">Postal
                Code
              </ui-textfield>
            </div>
            <google-map :class="`location-map`" :location="customer.billing_location"></google-map>
            <ui-divider :class="`location-divider`">
              <ui-form-field>
                <ui-checkbox :input-id="`billing-contact-same-as-customer-contact`"
                             v-model="customer.billing_location.contact_same_as_customer"
                             type="checkbox"></ui-checkbox>
                <label :for="`billing-contact-same-as-customer-contact`">Contact Same as Customer</label>
              </ui-form-field>
            </ui-divider>
            <div :class="`location-contacts`" v-if="!customer.billing_location.contact_same_as_customer">
              <h3 :class="$tt('headline5')">Contact(s)</h3>
              <div class="contact" v-for="(contact, index) in customer.billing_location.contacts" :key="index"
                   :contact="contact">
                <ui-textfield v-model="contact.first_name">First Name</ui-textfield>
                <ui-textfield v-model="contact.last_name">Last Name</ui-textfield>
                <ui-textfield v-model="contact.emails[0]" type="email">Email
                  <template #after>
                    <ui-textfield-icon>email</ui-textfield-icon>
                  </template>
                </ui-textfield>
                <ui-textfield v-model="customer.billing_location.contacts.phone_numbers[0]"
                              pattern="\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$" type="tel"
                >Phone
                  <template #after>
                    <ui-textfield-icon>phone</ui-textfield-icon>
                  </template>
                </ui-textfield>
              </div>
            </div>
          </div>
        </ui-card>
        <ui-form-field :class="actionClass">
          <ui-button raised @click="submit">Submit</ui-button>
        </ui-form-field>
      </ui-card>
    </template>
  </ui-form>

</template>

<script>
import {useValidator} from "balm-ui";
import GoogleMapAutoComplete from "@/components/shared/GoogleMapAutoComplete";
import GoogleMap from "@/components/shared/GoogleMap";
import {Customer} from "@/models/customer.ts";
import {Location} from "@/models/location.ts";

const validations = {
  first_name: {
    label: 'First Name',
    validator: 'required',
  },
  last_name: {
    label: 'Last Name',
    validator: 'required'
  },
  email: {
    label: 'Email',
    validator: 'required',
  },
  phone_number: {
    label: 'Phone Number',
    validator: 'required, phone_number'
  }

}
export default {
  name: "CustomerAdminCreateView",
  components: {GoogleMap, GoogleMapAutoComplete},
  data() {
    return {
      validMsg: {},
      validator: useValidator(),
      validations: validations,
      customer: new Customer(),
      billing_location_same_as_service_location: true,
      message: "",
      valid: false
    }
  },
  created() {
  },
  methods: {
    submit() {
      let result = this.validator.validate(this.customer)

      let {valid, validMsg} = result;
      this.validMsg = validMsg;
      this.$store.dispatch('customers/create', this.customer)

      if (valid) {
        this.$toast('ok');
      }
    },
    setLocation({location, ...data}) {
      location.address_line_1 = data.address_line_1
      location.name = data.name
      location.latitude = data.latitude
      location.longitude = data.longitude
      location.postal_code = data.postal_code
      location.state = data.state
      location.city = data.city
    },
  },
  watch: {
    billing_location_same_as_service_location(value) {
      if (!value && !this.customer.billing_location) {
        this.customer.billing_location = new Location()
      }
    }
  }
}
</script>

<style scoped lang="scss">
.mdc-card {
  margin: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  padding-bottom: 1rem;
}

h2, h3, h4, h5 {
}

.location {
  display: grid;
  grid-template-areas: "inputs  map"
  "inputs  map"
  "divider  divider"
"contacts contacts";
  justify-items: center;
}

.location-inputs {
  grid-area: inputs;
  align-content: space-evenly;
  justify-content: space-around;
  align-items: center;
  display: grid;
  grid-template-areas: "address-line-1 address-line-1 address-line-1"
"address-line-2 address-line-2 address-line-2"
"city state postal-code";
}

.location-map {
  grid-area: map;
}

.location-divider {
  grid-area: divider;
}

.location-contacts {
  grid-area: contacts;
}

.location-address-line-1 {
  grid-area: address-line-1
}

.location-address-line-2 {
  grid-area: address-line-2
}

.location-city {
  grid-area: city
}

.location-state {
  grid-area: state
}

.location-postal-code {
  grid-area: postal-code
}

</style>