import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import TicketTable from "@/components/TicketTable";
// import tickets from "@/lib/db/tickets";

export default async function Page() {
  const ticketStatusVocabulary = {
    open: "open",
    pending: "pending",
    new: "new",
    autoAnswered: "auto_answered",
    closed: "closed",
  };
  const apiResponse = await fetch(
    "https://suppercx.thefullstack.digital/tickets"
  );
  let tickets = await apiResponse.json();

  tickets = tickets.map((ticket) => ({
    id: ticket.id,
    title: ticket.description,
    source: ticket.source,
    status: ticket.status,
    originalLanguage: ticket.original_language,
    messages: ticket.messages.map((message) => ({
      id: message.id,
      sender: message.sender,
      email: message.email,
      body: message.body,
      sentDateTime: message.sent_date_time,
    })),
  }));

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">
          Inbox{" "}
          <span className="text-sm font-normal bg-muted text-muted-foreground px-2 py-1 rounded-full">
            {tickets.length}
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
          <TabsContent value="needs-supervision">
            <TicketTable
              data={tickets.filter((row) =>
                [
                  ticketStatusVocabulary.new,
                  ticketStatusVocabulary.open,
                  ticketStatusVocabulary.pending,
                ].includes(row.status)
              )}
            />
          </TabsContent>
          <TabsContent value="auto-answered">
            <TicketTable
              data={tickets.filter(
                (row) => row.status === ticketStatusVocabulary.autoAnswered
              )}
            />
          </TabsContent>
          <TabsContent value="closed-tickets">
            <TicketTable
              data={tickets.filter(
                (row) => row.status === ticketStatusVocabulary.closed
              )}
            />
          </TabsContent>
        </Tabs>
      </div>
    </>
  );
}
