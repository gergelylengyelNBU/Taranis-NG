<template>
    <v-row justify="center" class="attribute-value-layout pt-2"
           @mouseenter="itemHover = true"
           @mouseleave="itemHover = false"
    >
        <div class="col-left" style="position: relative;">
            <span v-if="itemHover" class="icon-tooltip">{{ modifiedTooltip }}</span>
            <slot name="col_left"></slot>
        </div>
        <div class="col-middle">
            <slot name="col_middle"></slot>
        </div>
        <div class="col-right">
            <slot name="col_right">
                <v-btn v-if="delButtonVisible" text small @click="del" :title="$t('report_item.tooltip.delete_value')">
                    <v-icon>mdi-close-circle</v-icon>
                </v-btn>
            </slot>
        </div>
    </v-row>
</template>

<script>
export default {
    name: "AttributeValueLayout",
    props: {
        del_button: null,
        val_index: null,
        occurrence: null,
        values: null
    },
    data: () => ({
        itemHover: false
    }),
    computed: {
        delButtonVisible() {
            return this.itemHover && !(this.occurrence >= this.values.length);
        },

        modifiedTooltip() {
            return this.values[this.val_index].user !== null ? this.values[this.val_index].last_updated + " " + this.values[this.val_index].user.name : ""
        }

    },
    methods: {
        del() {
            this.$emit('del-value');
        }
    }
}
</script>

<style>
.col-left {
    width: 8% !important;
}

.col-middle {
    width: 82% !important;
}

.col-right {
    width: 10% !important;
}

.col-left, .col-right {
    line-height: 2;
}

.attribute-value-layout:hover {
    background-color: rgba(106, 190, 242, 0.06);
}

.icon-tooltip {
    position: absolute;
    opacity: 0.7;
    top: -23px;
    left: -4px;
    font-size: 10px;
    width: 320px;
    color: #4694db;
}
</style>