import {defineStore} from 'pinia';


export const useItemsStore = defineStore('items', {
    state: () => ({
        items: {},
        paths: {},
        schema: undefined,
        editing: undefined,
        adding: false,
        tableMode: false,
        loading: false,
        savingItem: false,
    }),
    actions: {
        async retrieveItems($axios, apiUrl = undefined) {
            // Would be nice to amke ordering dynamic as a parameter, perhaps one day
            let ordering = "-updated_date"
            if (apiUrl.indexOf("/people/") !== -1)
                ordering = "first_name"

            this.items[apiUrl] = (await $axios.get(apiUrl + `?ordering=${ordering}`)).data
            return this.items[apiUrl]
        },
        async deleteItem($axios, apiUrl, id) {
            await $axios.delete(`${apiUrl}${id}`)
            await this.retrieveItems($axios, apiUrl)
        },
        async loadSchema($axios) {
            if (!this.schema) {
                const openAPI = (await $axios.get('/back/api/schema/?format=json')).data
                this.schema = openAPI.components.schemas
                this.paths = openAPI.paths
            }
        },
        async getSchemaDef($axios, apiUrl, resolveRefs = true, _schemaName = undefined) {
            await this.loadSchema($axios)
            let schemaName = _schemaName
            if (!schemaName)
                schemaName = this.getSchemaNameFromPath(apiUrl)
            if (resolveRefs)
                return await this.resolveRefs($axios, this.schema[schemaName])
            return this.schema[schemaName]
        },
        async requestOrGetItem($axios, apiUrl, filter, force = false) {
            if (force || !this.items[apiUrl]) {
                await this.retrieveItems($axios, apiUrl)
            }
            return this.items[apiUrl].find(item => {
                for (const [key, val] of Object.entries(filter)) {
                    if (item[key] === null && val === null)
                        continue
                    if (item[key] !== null && item[key].toString() !== val.toString())
                        return false
                }
                return true
            })
        },
        async requestOrGetItems($axios, apiUrl, filter, force = false) {
            if (force || !this.items[apiUrl]) {
                await this.retrieveItems($axios, apiUrl)
            }
            return this.items[apiUrl].filter(item => {
                for (const [key, val] of Object.entries(filter)) {
                    if (item[key] === null && val === null)
                        continue
                    if (item[key] !== null && val !== null && item[key].toString() !== val.toString())
                        return false
                }
                return true
            })
        },
        async upsertItem($axios, apiUrl, item) {
            this.savingItem = true
            if (item.id) {
                await $axios.patch(`${apiUrl}${item.id}/`, item)
            } else {
                await $axios.post(apiUrl, item)
            }
            await this.retrieveItems($axios, apiUrl)
            this.savingItem = false
        },
        async resolveRefs($axios, schema) {
            if (!schema.properties && schema.oneOf) {
                const oneOf = await this.getSchemaDef($axios, undefined, false, schema.oneOf[0].$ref.split("/").slice(-1)[0])
                schema.properties = oneOf.properties
                schema.required = oneOf.required
            }
            for (const [propName, propInfo] of Object.entries(schema.properties)) {
                let ref = propInfo.$ref || propInfo.items?.$ref
                if (ref) {
                    const refName = ref.split("/").slice(-1)[0]
                    let obj = await this.getSchemaDef($axios, undefined, false, refName)
                    if (obj.enum)  {
                        propInfo.choices = obj.enum.map((choice) => ({label: choice, value: choice}))
                    } else if (obj.type === 'object') {
                        let items = await this.retrieveItems($axios, this.getPathFromSchemaName(refName))
                        propInfo.choices = items.map((item) => ({label: item.name, value: item.id}))
                    }
                }
            }
            return schema
        },
        stateToRead(){
            this.editing = undefined
            this.adding = undefined
        }
    },
    getters: {
        getPathFromSchemaName: (state) => (schemaName) => {
            for (const [path, pathInfo] of Object.entries(state.paths)) {
                if (pathInfo.get?.responses &&
                    pathInfo.get?.responses['200']?.content &&
                    pathInfo.get?.responses['200']?.content['application/json']?.schema?.items?.$ref === `#/components/schemas/${schemaName}`) {
                    return path
                }
            }
        },
        getSchemaNameFromPath: (state) => (path) => {
            return state.paths[path].get?.responses['200']?.content['application/json']?.schema?.items?.$ref.split("/").slice(-1)[0]
        }
    }
});
