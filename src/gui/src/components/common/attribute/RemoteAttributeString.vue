<template>

    <div>
        <v-row v-for="(value, index) in values" :key="value.index" class="valueHolder">
            <v-col cols="11">
                <span>{{values[index].value}}</span>
            </v-col>
        </v-row>
    </div>

</template>

<script>
    export default {
        name: "RemoteAttributeString",
        props: {
            values: Array,
        },
    }
</script>

<style scoped>
    .valueHolder:hover {
        background-color: #f8f8f8;
        border-radius: 16px;
    }
</style>