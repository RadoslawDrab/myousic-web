export {}

declare global {
    export type RecursiveObject<T extends object, Key extends string = 'children'> = T & {
        [K in Key]?: RecursiveObject<T, Key>[]
    }

    export type VariableText<Value extends string, Prefix extends string = '', Suffix extends string = ''> = `${Prefix}${Value}${Suffix}`
}