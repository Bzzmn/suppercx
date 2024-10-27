"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Mail,
  Globe,
  Pencil,
  Plus,
  ArrowLeftRight,
  MessageCircle,
  Sparkles,
} from "lucide-react";

export default function TicketDetail({ ticket }) {
  const [response, setResponse] = useState("");
  const senderName = "Franco Parra";

  return (
    <div className="flex bg-background">
      <div className="flex-1 overflow-auto pr-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">{ticket.title}</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-muted-foreground">
              {new Date(ticket.messages[0].sentDateTime).toLocaleDateString(
                "en-US"
              )}
            </span>
            <Badge variant="secondary">DRAFT</Badge>
            {ticket.source === "Email" && (
              <div className="flex items-center">
                <Mail className="h-4 w-4 mr-2" />
                <span>Email</span>
              </div>
            )}
            {ticket.source === "WhatsApp" && (
              <div className="flex items-center">
                <MessageCircle className="h-4 w-4 mr-2" />
                <span>WhatsApp</span>
              </div>
            )}
            <div className="flex items-center">
              <Globe className="h-4 w-4 mr-2" />
              <span>{ticket.originalLanguage}</span>
            </div>
            <Button variant="outline">Close ticket</Button>
          </div>
        </div>

        {ticket.messages.map((message) => (
          <Card
            key={message.id}
            className={
              message.sender === "Support Team"
                ? "mb-6 bg-blue-50 ml-40"
                : "mb-6 mr-40"
            }
          >
            <CardHeader>
              <CardTitle>{message.sender}</CardTitle>
            </CardHeader>
            <CardContent>{message.body}</CardContent>
          </Card>
        ))}

        <div className="space-y-4 mt-2">
          <div className="flex space-x-2">
            <select className="border rounded p-2">
              <option>Normal</option>
            </select>
            <Button variant="outline" size="icon">
              <span className="font-bold">B</span>
            </Button>
            <Button variant="outline" size="icon">
              <span className="italic">I</span>
            </Button>
            <Button variant="outline" size="icon">
              <span className="underline">U</span>
            </Button>
            <Button variant="outline" size="icon">
              "
            </Button>
            <Button variant="outline" size="icon">
              A
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
              </svg>
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="21" y1="6" x2="3" y2="6"></line>
                <line x1="21" y1="12" x2="9" y2="12"></line>
                <line x1="21" y1="18" x2="7" y2="18"></line>
              </svg>
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="21" y1="10" x2="3" y2="10"></line>
                <line x1="21" y1="6" x2="3" y2="6"></line>
                <line x1="21" y1="14" x2="3" y2="14"></line>
                <line x1="21" y1="18" x2="3" y2="18"></line>
              </svg>
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
              </svg>
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </Button>
            <Button variant="outline" size="icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M4 7V4h16v3"></path>
                <path d="M9 20h6"></path>
                <path d="M12 4v16"></path>
              </svg>
            </Button>
          </div>
          <Textarea
            value={response}
            onChange={(e) => setResponse(e.target.value)}
            placeholder="Type your response here..."
            rows={10}
          />
          <div className="flex justify-between items-center">
            <span className="text-sm text-muted-foreground">
              {response.split(" ").length} words | {response.length} characters
            </span>
            <div>
              <span className="mr-2 text-sm text-muted-foreground">
                This answer will be translated to
              </span>
              <select className="border rounded p-2">
                <option>English</option>
              </select>
            </div>
          </div>
          <Button className="w-full">Send</Button>
        </div>
      </div>
      <div className="w-1/3 border-l pl-6 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Template info</CardTitle>
          </CardHeader>
          <CardContent>
            <h3 className="font-semibold mb-2 text-muted-foreground">
              The user cannot access his account
            </h3>
            <Badge variant="destructive" className="mb-4">
              0% Accuracy
            </Badge>
            <div className="grid grid-cols-2 gap-2">
              <Button variant="outline" className="w-full">
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Draft
              </Button>
              <Button variant="outline" className="w-full">
                <Pencil className="w-4 h-4 mr-2" />
                Edit
              </Button>
              <Button variant="outline" className="w-full">
                <Plus className="w-4 h-4 mr-2" />
                Create
              </Button>
              <Button variant="outline" className="w-full">
                <ArrowLeftRight className="w-4 h-4 mr-2" />
                Switch
              </Button>
            </div>
          </CardContent>
        </Card>
        <Card className="overflow-y-auto h-72">
          <CardHeader>
            <CardTitle>Template base</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">
              Hi {senderName}, Thank you for reaching out to the
              enricampos2020@gmail.comsupport team. We're sorry to hear that
              you're having trouble accessing your account, and we're here to
              help resolve this issue as quickly as possible. To assist you
              better, please follow the steps below: 1. Verify Your Credentials:
              - Ensure that you are entering the correct email address and
              password. Remember, passwords are case-sensitive. 2. Reset Your
              Password: - If you don't remember your password, please use the
              "Forgot Password?" option on the login page. You will receive an
              email with instructions to set up a new password. 3. Check Your
              Email: - Make sure that the email associated with your account is
              active, and check your inbox and spam/junk folders for our
              messages. If you still cannot access your account after following
              these steps, please provide us with the following information so
              we can investigate further: - A detailed description of the issue.
              - Any error messages you may have received (if applicable). - The
              browser or device you are using. The information you provide will
              help us expedite the resolution process. Once we have these
              details, we'll do our best to resolve your account access issue
              promptly. Thank you for your patience and for being a part of
              [Company Name]. We're here to assist you with anything you need.
              Best regards, enricampos2020 enricampos2020
              enricampos2020@gmail.com Support Team
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
