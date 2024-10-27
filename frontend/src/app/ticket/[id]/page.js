import TicketDetail from "@/components/TicketDetail";
import tickets from "@/lib/db/tickets";

export default async function Page({ params }) {
  const { id } = await params;
  const apiResponse = await fetch(
    "https://suppercx.thefullstack.digital/tickets"
  );
  const tickets = await apiResponse.json();
  let ticket = tickets.find((ticket) => ticket.id == id);
  ticket = {
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
  };

  return <TicketDetail ticket={ticket} />;
}
