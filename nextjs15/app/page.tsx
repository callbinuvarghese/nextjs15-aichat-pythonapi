import { ChatDemo } from "@/components/chat-demo";
import Image from "next/image";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export default function Home() {
  return ( // Parentheses are crucial here
    <main className="flex flex-col items-center justify-center p-12 max-w-3xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>
          <ChatDemo />
        </CardContent>
        <CardFooter>
          <p>Card Footer</p>
        </CardFooter>
      </Card>
    </main>
  );
}