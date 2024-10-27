import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Moon, LogOut, Mail } from "lucide-react";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function TicketDashboard() {
  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">
          Inbox{" "}
          <span className="text-sm font-normal bg-muted text-muted-foreground px-2 py-1 rounded-full">
            1
          </span>
        </h1>
        <div className="flex items-center space-x-2">
          <Input
            className="w-64"
            placeholder="Search by address or subject"
            type="search"
          />
          <Button>Reload tickets</Button>
        </div>
      </div>
      <div className="mb-6">
        <Tabs defaultValue="needs-supervision">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="needs-supervision">
              <Link href="#" className="text-sm font-medium">
                Needs supervision
              </Link>
            </TabsTrigger>
            <TabsTrigger value="auto-answered">
              <Link href="#" className="text-sm font-medium">
                Auto answered
              </Link>
            </TabsTrigger>
            <TabsTrigger value="closed-tickets">
              <Link href="#" className="text-sm font-medium">
                Closed tickets
              </Link>
            </TabsTrigger>
          </TabsList>
          <TabsContent value="needs-supervision">Needs supervision</TabsContent>
          <TabsContent value="auto-answered">Auto answered</TabsContent>
          <TabsContent value="closed-tickets">Closed tickets</TabsContent>
        </Tabs>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Info</TableHead>
            <TableHead>Origin</TableHead>
            <TableHead>Messages</TableHead>
            <TableHead>Original Language</TableHead>
            <TableHead>Last message</TableHead>
            <TableHead>Sender</TableHead>
            <TableHead>Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell className="font-medium">
              I am having trouble accessing the website
              <br />
              <span className="text-sm text-muted-foreground">
                Hi, I'm trying to access the website but it won't...
              </span>
            </TableCell>
            <TableCell>
              <Mail className="h-5 w-5 text-muted-foreground" />
              <span className="sr-only">Gmail</span>
            </TableCell>
            <TableCell>1</TableCell>
            <TableCell>
              <span className="flex items-center">
                <span className="w-2 h-2 mr-2 rounded-full bg-muted" />
                English
              </span>
            </TableCell>
            <TableCell>en alrededor de 3 horas</TableCell>
            <TableCell>
              <div className="flex items-center">
                <span className="w-8 h-8 mr-2 rounded-full bg-muted flex items-center justify-center text-muted-foreground">
                  G
                </span>
                <div>
                  <div className="font-medium">Gurusup</div>
                  <div className="text-sm text-muted-foreground">
                    demo@gurusup.com
                  </div>
                </div>
              </div>
            </TableCell>
            <TableCell>
              <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-yellow-100 text-yellow-800">
                PENDING
              </span>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <div className="flex items-center justify-between mt-6">
        <Button variant="ghost">Previous</Button>
        <span className="text-sm text-muted-foreground">1</span>
        <Button variant="ghost">Next</Button>
      </div>
    </>
  );
}
