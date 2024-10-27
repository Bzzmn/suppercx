import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Inbox, PlusCircle } from "lucide-react";

export default function EmptyState() {
  return (
    <Card className="w-full max-w-2xl mx-auto mt-10">
      <CardContent className="flex flex-col items-center justify-center p-12 text-center">
        <Inbox className="w-16 h-16 text-muted-foreground mb-6" />
        <h2 className="text-2xl font-bold mb-2">No pending tickets</h2>
        <p className="text-muted-foreground mb-6">
          When new tickets arrive, they will appear here. In the meantime, why
          not create a test ticket?
        </p>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" />
          Create test ticket
        </Button>
      </CardContent>
    </Card>
  );
}
