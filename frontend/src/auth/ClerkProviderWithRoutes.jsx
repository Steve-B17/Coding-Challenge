import {ClerkProvider} from "@clerk/clerk-react"

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

export default function ClerkProviderWithRoutes({children}) {
    return (
        <ClerkProvider publishableKey={clerkPubKey}>
            {children}
        </ClerkProvider>
    )
}
