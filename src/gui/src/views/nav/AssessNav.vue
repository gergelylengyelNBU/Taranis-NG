<template>
    <Navigation
            :links="links"
            :icon="'mdi-google-circles-extended'"
    />
</template>

<script>
    import Navigation from "../../components/common/Navigation";

    export default {
        name: "AssessNav",
        components: {
            Navigation
        },
        data: () => ({
            groups: [],
            links: []
        }),
        mounted() {
            this.$store.dispatch('getAllOSINTSourceGroupsAssess', {search:''})
                .then(() => {
                    this.groups = this.$store.getters.getOSINTSourceGroups.items;
                    for (let i = 0; i < this.groups.length; i++) {
                        this.links.push({
                            icon: 'mdi-folder-multiple',
                            title: this.groups[i].name,
                            route: '/assess/group/' + this.groups[i].id,
                            id: this.groups[i].id
                        })
                    }

                    if (!window.location.pathname.includes("/group/") && this.links.length > 0) {

                        this.$router.push(this.links[0].route)
                    }
                });
        }
    }
</script>
