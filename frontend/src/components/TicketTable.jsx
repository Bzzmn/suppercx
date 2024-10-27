"use client";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Mail, MessageCircle } from "lucide-react";
import humanizeDuration from "humanize-duration";
import { Badge } from "@/components/ui/badge";
import EmptyState from "./EmptyState";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useRouter } from "next/navigation";

export default function TicketTable({ data }) {
  const router = useRouter();

  if (data.length === 0) {
    return <EmptyState />;
  }

  const handleRowClick = (ticketId) => {
    router.push(`/ticket/${ticketId}`);
  };

  return (
    <>
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
          {data.map((row) => (
            <TableRow key={row.id} onClick={() => handleRowClick(row.id)}>
              <TableCell className="font-medium">
                {row.title}
                <p className="text-sm text-muted-foreground w-96 overflow-hidden text-ellipsis whitespace-nowrap">
                  {row.messages[0].body}
                </p>
              </TableCell>
              <TableCell>
                {row.source === "Email" && (
                  <>
                    <Mail className="h-5 w-5 text-muted-foreground" />
                    <span className="sr-only">Gmail</span>
                  </>
                )}
                {row.source === "WhatsApp" && (
                  <>
                    <MessageCircle className="h-5 w-5 text-muted-foreground" />
                    <span className="sr-only">WhatsApp</span>
                  </>
                )}
              </TableCell>
              <TableCell>{row.messages.length}</TableCell>
              <TableCell>
                <span className="flex items-center">
                  <span className="w-2 h-2 mr-2 rounded-full bg-muted" />
                  {row.originalLanguage}
                </span>
              </TableCell>
              <TableCell>
                {humanizeDuration(
                  new Date().getTime() -
                    new Date(row.messages.slice(-1)[0].sentDateTime).getTime(),
                  { largest: 1 }
                )}
              </TableCell>
              <TableCell>
                <div className="flex items-center">
                  <span className="w-8 h-8 mr-2 rounded-full bg-muted flex items-center justify-center text-muted-foreground">
                    G
                  </span>
                  <div>
                    <div className="font-medium">
                      {row.messages.slice(-1)[0].sender}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {row.messages.slice(-1)[0].email}
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                {row.status === "Pending" && <Badge>Pending</Badge>}
                {row.status === "Closed" && <Badge>Closed</Badge>}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination className="mt-2">
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href="#" />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">1</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext href="#" />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </>
  );
}
