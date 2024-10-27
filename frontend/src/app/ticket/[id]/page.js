import TicketDetail from "@/components/TicketDetail";
import tickets from "@/lib/db/tickets";

export default async function Page({ params }) {
  const { id } = await params;
  const ticket = tickets.find((ticket) => ticket.id == id);

  return <TicketDetail ticket={ticket} />;
}
