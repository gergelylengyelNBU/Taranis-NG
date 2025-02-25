<template>
    <div>
        <v-btn v-if="canCreate" depressed small color="white--text ma-2 mt-3 mr-5" @click="addNode">
            <v-icon left>mdi-plus-circle-outline</v-icon>
            <span class="subtitle-2">{{$t('presenters_node.add_btn')}}</span>
        </v-btn>
        <v-row justify="center">
            <v-dialog v-model="visible" max-width="600" persistent>
                <v-card>

                    <v-toolbar dark color="primary">
                        <v-btn icon dark @click="cancel">
                            <v-icon>mdi-close-circle</v-icon>
                        </v-btn>
                        <v-toolbar-title v-if="!edit">{{$t('presenters_node.add_new')}}</v-toolbar-title>
                        <v-toolbar-title v-if="edit">{{$t('presenters_node.edit')}}</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn v-if="canUpdate" text type="submit" form="form">
                            <v-icon left>mdi-content-save</v-icon>
                            <span>{{$t('presenters_node.save')}}</span>
                        </v-btn>
                    </v-toolbar>

                    <v-card-text>
                        <v-form @submit.prevent="add" id="form" ref="form">


                            <v-text-field :disabled="!canUpdate"
                                    :label="$t('presenters_node.name')"
                                    name="name"
                                    type="text"
                                    v-model="node.name"
                                    v-validate="'required'"
                                    data-vv-name="name"
                                    :error-messages="errors.collect('name')"
                                    :spellcheck="$store.state.settings.spellcheck"
                            ></v-text-field>
                            <v-textarea :disabled="!canUpdate"
                                    :label="$t('presenters_node.description')"
                                    name="description"
                                    v-model="node.description"
                                    :spellcheck="$store.state.settings.spellcheck"
                            ></v-textarea>
                            <v-text-field :disabled="!canUpdate"
                                    :label="$t('presenters_node.url')"
                                    name="url"
                                    type="text"
                                    v-model="node.api_url"
                                    v-validate="'required'"
                                    data-vv-name="url"
                                    :error-messages="errors.collect('url')"
                            ></v-text-field>
                            <v-text-field :disabled="!canUpdate"
                                    :label="$t('presenters_node.key')"
                                    name="key"
                                    type="text"
                                    v-model="node.api_key"
                                    v-validate="'required'"
                                    data-vv-name="key"
                                    :error-messages="errors.collect('key')"
                            ></v-text-field>

                            <v-alert v-if="show_validation_error" dense type="error" text>
                                {{$t('presenters_node.validation_error')}}
                            </v-alert>
                            <v-alert v-if="show_error" dense type="error" text>{{$t('presenters_node.error')}}
                            </v-alert>
                        </v-form>
                    </v-card-text>

                </v-card>
            </v-dialog>
        </v-row>
    </div>
</template>

<script>
    import {createNewPresentersNode} from "@/api/config";
    import {updatePresentersNode} from "@/api/config";
    import AuthMixin from "@/services/auth/auth_mixin";
    import Permissions from "@/services/auth/permissions";

    export default {
        name: "NewPresentersNode",
        data: () => ({
            visible: false,
            edit: false,
            show_validation_error: false,
            show_error: false,
            node: {
                id: "",
                name: "",
                description: "",
                api_url: "",
                api_key: ""
            }
        }),
        mixins: [AuthMixin],
        computed: {
            canCreate() {
                return this.checkPermission(Permissions.CONFIG_PRESENTERS_NODE_CREATE)
            },
            canUpdate() {
                return this.checkPermission(Permissions.CONFIG_PRESENTERS_NODE_UPDATE) || !this.edit
            },
        },
        methods: {
            addNode() {
                this.visible = true
                this.edit = false
                this.show_error = false;
                this.node.name = ""
                this.node.description = ""
                this.node.api_url = ""
                this.node.api_key = ""
                this.$validator.reset();
            },

            cancel() {
                this.$validator.reset();
                this.visible = false
            },

            add() {
                this.$validator.validateAll().then(() => {

                    if (!this.$validator.errors.any()) {

                        this.show_validation_error = false;
                        this.show_error = false;

                        if (this.edit) {

                            updatePresentersNode(this.node).then(() => {

                                this.$validator.reset();
                                this.visible = false;
                                this.$root.$emit('notification',
                                    {
                                        type: 'success',
                                        loc: 'presenters_node.successful_edit'
                                    }
                                )
                            }).catch(() => {

                                this.show_error = true;
                            })

                        } else {
                            createNewPresentersNode(this.node).then(() => {

                                this.$validator.reset();
                                this.visible = false;
                                this.$root.$emit('notification',
                                    {
                                        type: 'success',
                                        loc: 'presenters_node.successful'
                                    }
                                )
                            }).catch(() => {

                                this.show_error = true;
                            })
                        }
                    } else {

                        this.show_validation_error = true;
                    }

                })
            }
        },
        mounted() {
            this.$root.$on('show-edit', (data) => {
                this.visible = true;
                this.edit = true;
                this.show_error = false;
                this.node.id = data.id;
                this.node.name = data.name;
                this.node.description = data.description;
                this.node.api_url = data.api_url;
                this.node.api_key = data.api_key;
            });
        },
        beforeDestroy() {
            this.$root.$off('show-edit')
        }
    }
</script>
